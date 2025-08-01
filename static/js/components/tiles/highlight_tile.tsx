/**
 * Copyright 2023 Google LLC
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
 * Component for rendering a highlight tile.
 */

import _ from "lodash";
import React, { ReactElement, useEffect, useRef, useState } from "react";

import {
  ASYNC_ELEMENT_CLASS,
  ASYNC_ELEMENT_HOLDER_CLASS,
} from "../../constants/css_constants";
import { formatNumber, translateUnit } from "../../i18n/i18n";
import { Observation, StatMetadata } from "../../shared/stat_types";
import {
  NamedTypedPlace,
  StatVarFacetMap,
  StatVarSpec,
} from "../../shared/types";
import { TileSources } from "../../tools/shared/metadata/tile_sources";
import { FacetMetadata } from "../../types/facet_metadata";
import { getPoint, getSeries } from "../../utils/data_fetch_utils";
import { formatDate } from "../../utils/string_utils";
import {
  formatString,
  getDenomInfo,
  getNoDataErrorMsg,
  getStatFormat,
  ReplacementStrings,
} from "../../utils/tile_utils";

// units that should be formatted as part of the number
const NUMBER_UNITS = ["%"];

export interface HighlightTilePropType {
  // API root for data fetch
  apiRoot?: string;
  // Date to fetch data for
  date?: string;
  // Text to accompany the stat var value highlighted
  description: string;
  // Place to get data for
  place: NamedTypedPlace;
  // Variable to get data for
  statVarSpec: StatVarSpec;
  // Optional: Override sources for this tile
  sources?: string[];
  // Facet metadata to use for the highlight tile
  highlightFacet?: FacetMetadata;
}

export interface HighlightData extends Observation {
  // A set of string sources (URLs)
  sources: Set<string>;
  // A full set of the facets used within the chart
  facets: Record<string, StatMetadata>;
  // A mapping of which stat var used which facets
  statVarToFacets: StatVarFacetMap;
  numFractionDigits?: number;
  errorMsg: string;
}

export function HighlightTile(props: HighlightTilePropType): ReactElement {
  const containerRef = useRef(null);
  const [highlightData, setHighlightData] = useState<HighlightData | undefined>(
    null
  );

  const {
    statVarSpec,
    place,
    highlightFacet,
    apiRoot,
    description: highlightDesc,
  } = props;

  useEffect(() => {
    (async (): Promise<void> => {
      try {
        const data = await fetchData(
          place,
          statVarSpec,
          highlightFacet,
          apiRoot
        );
        setHighlightData(data);
      } catch {
        setHighlightData(null);
      }
    })();
  }, [apiRoot, highlightFacet, place, statVarSpec, highlightDesc]);

  if (!highlightData) {
    return null;
  }
  const description = getDescription(highlightData, props);
  // TODO: The {...{ part: "container"}} syntax to set a part is a hacky
  // workaround to add a "part" attribute to a React element without npm errors.
  // This hack should be cleaned up.
  let numberUnit = "";
  let metadataUnit = translateUnit(
    props.statVarSpec.unit || highlightData.unitDisplayName
  );
  if (metadataUnit) {
    numberUnit = NUMBER_UNITS.find((unit) => metadataUnit.startsWith(unit));
    metadataUnit = numberUnit
      ? metadataUnit.slice(numberUnit.length).trimStart()
      : metadataUnit;
  }
  return (
    <div
      className={`chart-container highlight-tile ${ASYNC_ELEMENT_HOLDER_CLASS}`}
      {...{ part: "container" }}
      ref={containerRef}
    >
      {highlightData && !highlightData.errorMsg && (
        <>
          <span className="stat">
            <span className={`number ${ASYNC_ELEMENT_CLASS}`}>
              {formatNumber(
                highlightData.value,
                numberUnit,
                false,
                highlightData.numFractionDigits
              )}
            </span>
            {metadataUnit && <span className="metadata">{metadataUnit}</span>}
          </span>
        </>
      )}
      <span className="desc">{description}</span>
      {highlightData && highlightData.errorMsg && (
        <span>{highlightData.errorMsg}</span>
      )}
      {!_.isEmpty(highlightData.sources) && !highlightData.errorMsg && (
        <TileSources
          apiRoot={props.apiRoot}
          containerRef={containerRef}
          sources={props.sources || highlightData.sources}
          facets={highlightData.facets}
          statVarToFacets={highlightData.statVarToFacets}
          statVarSpecs={[props.statVarSpec]}
        />
      )}
    </div>
  );
}

export function getDescription(
  highlightData: HighlightData,
  props: HighlightTilePropType
): string {
  const rs: ReplacementStrings = {
    placeName: props.place.name || "",
    date: highlightData.date ? formatDate(highlightData.date) : "",
  };
  let description = "";
  if (props.description) {
    const dateString =
      !props.description.includes("${date}") && rs.date ? " (${date})" : "";
    description = formatString(props.description + dateString, rs);
  }
  return description;
}

export const fetchData = async (
  place: NamedTypedPlace,
  statVarSpec: StatVarSpec,
  highlightFacet: FacetMetadata,
  apiRoot?: string
): Promise<HighlightData> => {
  const facetId = highlightFacet
    ? undefined
    : statVarSpec.facetId
    ? [statVarSpec.facetId]
    : undefined;
  // Now assume highlight only talks about one stat var.
  const statPromise = getPoint(
    apiRoot,
    [place.dcid],
    [statVarSpec.statVar],
    statVarSpec.date,
    undefined,
    highlightFacet,
    facetId
  );
  const denomPromise = statVarSpec.denom
    ? getSeries(apiRoot, [place.dcid], [statVarSpec.denom], [], highlightFacet)
    : Promise.resolve(null);
  const [statResp, denomResp] = await Promise.all([statPromise, denomPromise]);
  const mainStatData = _.isArray(statResp.data[statVarSpec.statVar][place.dcid])
    ? statResp.data[statVarSpec.statVar][place.dcid][0]
    : statResp.data[statVarSpec.statVar][place.dcid];
  let value = mainStatData.value;

  const facets: Record<string, StatMetadata> = {};
  const statVarToFacets: StatVarFacetMap = {};

  const facet = statResp.facets[mainStatData.facet];

  if (mainStatData.facet && facet) {
    facets[mainStatData.facet] = facet;
    if (!statVarToFacets[statVarSpec.statVar]) {
      statVarToFacets[statVarSpec.statVar] = new Set();
    }
    statVarToFacets[statVarSpec.statVar].add(mainStatData.facet);
  }

  const sources = new Set<string>();
  if (facet && facet.provenanceUrl) {
    sources.add(facet.provenanceUrl);
  }
  const { unit, scaling, numFractionDigits } = getStatFormat(
    statVarSpec,
    statResp
  );
  let numFractionDigitsUsed: number;
  if (statVarSpec.denom) {
    const denomInfo = getDenomInfo(
      statVarSpec,
      denomResp,
      place.dcid,
      mainStatData.date
    );
    if (denomInfo && value) {
      value /= denomInfo.value;
      sources.add(denomInfo.source);
    } else {
      value = null;
    }
  }
  let errorMsg = "";
  if (_.isUndefined(value) || _.isNull(value)) {
    errorMsg = getNoDataErrorMsg([statVarSpec]);
  } else {
    // Only do additional calculations if value is not null or undefined
    // If value is a decimal, calculate the numFractionDigits as the number of
    // digits to get the first non-zero digit and the number after
    // TODO: think about adding a limit to the number of digits.
    numFractionDigitsUsed =
      Math.abs(value) >= 1 || value === 0
        ? numFractionDigits
        : 1 - Math.floor(Math.log(Math.abs(value)) / Math.log(10));
    if (scaling) {
      value *= scaling;
    }
  }
  return {
    value,
    date: mainStatData.date,
    numFractionDigits: numFractionDigitsUsed,
    unitDisplayName: unit,
    sources,
    facets,
    statVarToFacets,
    errorMsg,
  };
};
