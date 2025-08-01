# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Endpoints for Datacommons NL"""

import copy
import json
import time
from typing import Dict

import flask
from flask import Blueprint
from flask import current_app
from flask import request
from flask import Response

from server.lib.cache import cache
from server.lib.nl.common import serialize
import server.lib.nl.common.bad_words as bad_words
import server.lib.nl.common.constants as constants
import server.lib.nl.common.counters as ctr
import server.lib.nl.common.utils as utils
import server.lib.nl.common.utterance as nl_utterance
import server.lib.nl.config_builder.base as config_builder
import server.lib.nl.detection.detector as nl_detector
from server.lib.nl.detection.utils import create_utterance
from server.lib.nl.explore import overview
from server.lib.nl.explore import related
import server.lib.nl.explore.fulfiller_bridge as nl_fulfillment
from server.lib.nl.explore.params import Clients
from server.lib.nl.explore.params import DCNames
from server.lib.nl.explore.params import Params
from server.lib.util import get_nl_disaster_config
from server.lib.util import post_body_cache_key
from server.routes import TIMEOUT
from server.routes.explore import helpers
import server.services.bigtable as bt

bp = Blueprint('explore_api', __name__, url_prefix='/api/explore')


#
# The detection endpoint.
#
@bp.route('/detect', methods=['POST'])
def detect():
  debug_logs = {}
  client = request.args.get(Params.CLIENT.value, Clients.DEFAULT.value)

  utterance, error_json = helpers.parse_query_and_detect(
      request, 'explore', client, debug_logs)
  if error_json:
    return error_json

  data_dict = copy.deepcopy(utterance.insight_ctx)
  utterance.prev_utterance = None
  data_dict[Params.CTX.value] = serialize.save_utterance(utterance)

  dbg_counters = utterance.counters.get()
  utterance.counters = None
  status_str = "Successful"

  return helpers.prepare_response_common(data_dict,
                                         status_str,
                                         utterance.detection,
                                         dbg_counters,
                                         debug_logs,
                                         has_data=True,
                                         test=utterance.test,
                                         client=client)


#
# The fulfillment endpoint.
#
# POST request should contain:
#  - entities: An ordered list of places or other entity DCIDs.
#  - variables: A ordered list of SV or topic (dc/topic/..) DCIDs.
#  - childEntityType: A type of child entity (optional)
#
@bp.route('/fulfill', methods=['POST'])
def fulfill():
  """Data handler."""
  debug_logs = {}
  counters = ctr.Counters()
  return _fulfill_with_insight_ctx(request, debug_logs, counters)


#
# The detect and fulfill endpoint.
#
@bp.route('/detect-and-fulfill', methods=['POST'])
def detect_and_fulfill():
  debug_logs = {}

  test = request.args.get(Params.TEST.value, '')
  client = request.args.get(Params.CLIENT.value, Clients.DEFAULT.value)

  # First sanity DC name, if any.
  dc_name = request.get_json().get(Params.DC.value)
  if not dc_name:
    dc_name = DCNames.MAIN_DC.value
  if dc_name not in set([it.value for it in DCNames]):
    return helpers.abort(f'Invalid Custom Data Commons Name {dc_name}',
                         '', [],
                         test=test,
                         client=client)

  utterance, error_json = helpers.parse_query_and_detect(
      request, 'explore', client, debug_logs)
  if error_json:
    return error_json

  # Set some params used downstream in explore flow.
  utterance.insight_ctx[
      Params.EXP_MORE_DISABLED.value] = request.get_json().get(
          Params.EXP_MORE_DISABLED, "")
  utterance.insight_ctx[Params.SKIP_RELATED_THINGS] = request.args.get(
      Params.SKIP_RELATED_THINGS.value, '') == 'true'
  helpers.update_insight_ctx_for_chart_fulfill(request, utterance, dc_name)

  # Important to setup utterance for explore flow (this is really the only difference
  # between NL and Explore).
  start = time.time()
  nl_detector.setup_for_explore(utterance)
  utterance.counters.timeit('setup_for_explore', start)

  return _fulfill_with_chart_config(utterance, debug_logs)


#
# The follow up question endpoint that generates questions
# based off of the initial query and topics found in the related topics.
#
@bp.route('/follow-up-questions', methods=['POST'])
@cache.cached(timeout=TIMEOUT, make_cache_key=post_body_cache_key)
def follow_up_questions():

  initial_query = request.get_json().get('q', '')
  related_topics = request.get_json().get('relatedTopics', [])

  if not initial_query:
    return Response(json.dumps({'error': 'Missing query in request.'}),
                    400,
                    mimetype="application/json")
  if not related_topics:
    return Response(json.dumps({'error': 'Missing related topics in request.'}),
                    400,
                    mimetype="application/json")

  generated_questions = related.generate_follow_up_questions(
      query=initial_query, related_topics=related_topics)

  # Checks for adversarial questions
  safe_generated_questions = [
      question for question in generated_questions
      if bad_words.is_safe(query=question,
                           bad_words=current_app.config['NL_BAD_WORDS'])
  ]

  return Response(json.dumps({'follow_up_questions': safe_generated_questions}),
                  200,
                  mimetype="application/json")


# The page overview endpoint that generates an introductory paragraph
# based off of the initial query and relevant statistical variables.
#
@bp.route('/page-overview', methods=['POST'])
@cache.cached(timeout=TIMEOUT, make_cache_key=post_body_cache_key)
def page_overview():

  initial_query = request.get_json().get('q', '')
  stat_vars = request.get_json().get('statVars', [])

  if not initial_query:
    return Response(json.dumps({'error': 'Missing query in request.'}),
                    400,
                    mimetype="application/json")
  if not stat_vars:
    return Response(json.dumps(
        {'error': 'Missing statistical variables in request.'}),
                    400,
                    mimetype="application/json")

  generated_overview = overview.generate_page_overview(query=initial_query,
                                                       stat_vars=stat_vars)

  if not generated_overview:
    return Response(json.dumps(
        {'error': "Page overview could not be generated at this time."}),
                    503,
                    mimetype="application/json")

  return Response(json.dumps({'page_overview': generated_overview}),
                  200,
                  mimetype="application/json")


#
# Given an utterance constructed either from a query or from dcids,
# fulfills it into charts.
#
def _fulfill_with_chart_config(utterance: nl_utterance.Utterance,
                               debug_logs: Dict) -> Dict:
  disaster_config = current_app.config['NL_DISASTER_CONFIG']
  if current_app.config['LOCAL']:
    # Reload configs for faster local iteration.
    disaster_config = get_nl_disaster_config()

  cb_config = config_builder.Config(
      event_config=disaster_config,
      sv_chart_titles=current_app.config['NL_CHART_TITLES'],
      nopc_vars=current_app.config['NOPC_VARS'],
      sdg_percent_vars=current_app.config['SDG_PERCENT_VARS'])

  start = time.time()
  fresp = nl_fulfillment.fulfill(utterance, cb_config)
  utterance.counters.timeit('fulfillment', start)

  return helpers.prepare_response(utterance,
                                  fresp.chart_pb,
                                  utterance.detection,
                                  debug_logs,
                                  fresp.related_things,
                                  fulfill_user_msg=fresp.user_message)


#
# Given an insight context, fulfills it into charts.
#
# TODO: Add support for i18n.
def _fulfill_with_insight_ctx(request: Dict, debug_logs: Dict,
                              counters: ctr.Counters) -> Dict:
  insight_ctx = request.get_json()
  test = request.args.get(Params.TEST.value, '')
  client = request.args.get(Params.CLIENT.value, Clients.DEFAULT.value)
  mode = request.args.get(Params.MODE.value, '')
  if not insight_ctx:
    return helpers.abort('Sorry, could not answer your query.',
                         '', [],
                         test=test,
                         client=client)
  if not insight_ctx.get('entities'):
    return helpers.abort('Could not recognize any places in the query.',
                         '', [],
                         test=test,
                         client=client)

  entities = insight_ctx.get(Params.ENTITIES.value, [])
  cmp_entities = insight_ctx.get(Params.CMP_ENTITIES.value, [])
  vars = insight_ctx.get(Params.VARS.value, [])
  cmp_vars = insight_ctx.get(Params.CMP_VARS.value, [])
  child_type = insight_ctx.get(Params.CHILD_TYPE.value, '')
  session_id = insight_ctx.get(Params.SESSION_ID.value, '')
  classifications = insight_ctx.get(Params.CLASSIFICATIONS.value, [])

  dc_name = insight_ctx.get(Params.DC.value)
  if not dc_name:
    dc_name = DCNames.MAIN_DC.value
  if dc_name not in set([it.value for it in DCNames]):
    return helpers.abort(f'Invalid Custom Data Commons Name {dc_name}',
                         '', [],
                         test=test,
                         client=client)

  if not session_id:
    if current_app.config['LOG_QUERY']:
      session_id = utils.new_session_id('explore')
    else:
      session_id = constants.TEST_SESSION_ID

  # There is not detection, so just construct a structure.
  # TODO: Maybe check that if cmp_entities is set, entities should
  # be singleton.
  start = time.time()
  debug_logs = {}
  query_detection, error_msg = nl_detector.construct_for_explore(
      entities, vars, child_type, cmp_entities, cmp_vars, classifications,
      debug_logs, counters)
  counters.timeit('construct_for_explore', start)
  if not query_detection:
    return helpers.abort(error_msg, '', [], test=test, client=client)

  utterance = create_utterance(query_detection,
                               None,
                               counters,
                               session_id,
                               test=test,
                               client=client,
                               mode=mode)
  utterance.insight_ctx = insight_ctx
  helpers.update_insight_ctx_for_chart_fulfill(request, utterance, dc_name)
  return _fulfill_with_chart_config(utterance, debug_logs)
