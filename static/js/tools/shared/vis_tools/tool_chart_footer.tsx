/**
 * Copyright 2022 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/**
 * Footer for charts created by the different tools
 */

import _ from "lodash";
import React, { ReactElement, useState } from "react";
import { FormGroup, Input, Label } from "reactstrap";

import { intl } from "../../../i18n/i18n";
import { messages } from "../../../i18n/i18n_messages";
import {
  GA_EVENT_TOOL_CHART_OPTION_CLICK,
  GA_PARAM_TOOL_CHART_OPTION,
  GA_VALUE_TOOL_CHART_OPTION_PER_CAPITA,
  triggerGAEvent,
} from "../../../shared/ga_events";
import { urlToDisplayText } from "../../../shared/util";

interface ToolChartFooterProps {
  // Id of the chart this footer is being added to.
  chartId: string;
  // Sources the chart got its data from.
  sources: Set<string>;
  // Measurement methods of the data of the chart.
  mMethods: Set<string>;
  // Whether to hide isRatio option.
  hideIsRatio: boolean;
  // Whether or not the chart is showing per capita calculation.
  isPerCapita?: boolean;
  // Callback when isRatio is updated. Used when hideIsRatio is false.
  onIsPerCapitaUpdated?: (isPerCapita: boolean) => void;
  // children components
  children?: React.ReactNode;
}

const DOWN_ARROW_HTML = <i className="material-icons">expand_more</i>;
const UP_ARROW_HTML = <i className="material-icons">expand_less</i>;
const SELECTOR_PREFIX = "chart-footer";
const FEEDBACK_LINK = "/feedback";

export function ToolChartFooter(props: ToolChartFooterProps): ReactElement {
  const mMethods = !_.isEmpty(props.mMethods)
    ? Array.from(props.mMethods).join(", ")
    : "";
  const ratioCheckboxId = props.chartId + "-ratio";
  const [chartOptionsOpened, setChartOptionsOpened] = useState(true);

  return (
    <>
      <div
        className={`${SELECTOR_PREFIX}-container ${
          chartOptionsOpened ? "no-bottom-border" : ""
        }`}
      >
        <div className={`${SELECTOR_PREFIX}-metadata-section`}>
          {!_.isEmpty(props.sources) && (
            <div className={`${SELECTOR_PREFIX}-metadata`}>
              <span>Data from {getSourcesJsx(props.sources)}</span>
              {globalThis.viaGoogle
                ? " " + intl.formatMessage(messages.viaGoogle)
                : ""}
            </div>
          )}
          {!_.isEmpty(mMethods) && (
            <div className={`${SELECTOR_PREFIX}-metadata`}>
              <span>{`Measurement method${
                props.mMethods.size > 1 ? "s" : ""
              }: ${mMethods}`}</span>
            </div>
          )}
        </div>
        <div
          onClick={(): void => setChartOptionsOpened(!chartOptionsOpened)}
          className={`${SELECTOR_PREFIX}-options-button`}
        >
          <span>Chart Options</span>
          {chartOptionsOpened ? UP_ARROW_HTML : DOWN_ARROW_HTML}
        </div>
      </div>
      {chartOptionsOpened && (
        <div className={`${SELECTOR_PREFIX}-options-section`}>
          {!props.hideIsRatio && (
            <span className="chart-option">
              <FormGroup check>
                <Label check>
                  <Input
                    id={ratioCheckboxId}
                    type="checkbox"
                    checked={props.isPerCapita}
                    onChange={(): void => {
                      props.onIsPerCapitaUpdated(!props.isPerCapita);
                      if (!props.isPerCapita) {
                        triggerGAEvent(GA_EVENT_TOOL_CHART_OPTION_CLICK, {
                          [GA_PARAM_TOOL_CHART_OPTION]:
                            GA_VALUE_TOOL_CHART_OPTION_PER_CAPITA,
                        });
                      }
                    }}
                  />
                  Per Capita
                </Label>
              </FormGroup>
            </span>
          )}
          {props.children}
        </div>
      )}
      <div className="feedback-link">
        <a href={FEEDBACK_LINK}>Feedback</a>
      </div>
    </>
  );
}

function getSourcesJsx(sources: Set<string>): ReactElement[] {
  const sourceList: string[] = Array.from(sources);
  const seenSourceText = new Set();
  return sourceList.map((source, index) => {
    const sourceText = urlToDisplayText(source);
    if (seenSourceText.has(sourceText)) {
      return null;
    }
    seenSourceText.add(sourceText);
    // handle relative url that doesn't contain https or http or www
    const processedUrl = sourceText === source ? "https://" + source : source;
    return (
      <span key={source}>
        {index > 0 ? ", " : ""}
        <a href={processedUrl}>{sourceText}</a>
      </span>
    );
  });
}
