import { useState, useRef } from "react";
import MaterialTable, { MTableBody } from "material-table";
import {
  tableIcons,
  columns,
  FILTERABLE_COLUMNS,
  SORTABLE_COLUMNS,
} from "../utils/constants";
import {
  buildStatsQueryFromParams,
  buildExportAsExcelParams,
} from "../utils/utils";
import { saveAs } from "file-saver";

const NFLRushingTable = () => {
  const filtering = useRef({});
  const [ordering, setOrdering] = useState({});

  const RENDER_COLUMNS = columns.map((column) => {
    if (FILTERABLE_COLUMNS.includes(column.field)) {
      return {
        ...column,
        filtering: true,
        sorting: false,
      };
    }

    if (SORTABLE_COLUMNS.includes(column.field)) {
      return {
        ...column,
        filtering: false,
        customSort: () => {},
      };
    }

    return {
      ...column,
      filtering: false,
      sorting: false,
    };
  });

  const handleOrderCHange = (order, direction) => {
    if (order !== -1) {
      setOrdering({
        orderBy: { field: RENDER_COLUMNS[order].field },
        orderDirection: direction,
      });
    } else {
      setOrdering({});
    }
  };

  return (
    <MaterialTable
      title="NFL Rushing Stats"
      icons={tableIcons}
      columns={RENDER_COLUMNS}
      data={(query) =>
        new Promise((resolve, _) => {
          const url = buildStatsQueryFromParams(query);
          fetch(url, { mode: "cors" })
            .then((response) => response.json())
            .then((result) => {
              resolve({
                data: result.data,
                page: result.current - 1,
                totalCount: result.total,
              });
            });
        })
      }
      onOrderChange={handleOrderCHange}
      components={{
        Body: (props) => (
          <MTableBody
            {...props}
            onFilterChanged={(columnId, value) => {
              props.onFilterChanged(columnId, value);
              filtering.current = { value };
            }}
          />
        ),
      }}
      options={{
        filtering: true,
        sorting: true,
        paging: true,
        padding: "dense",
        exportButton: { csv: true },
        exportAllData: true,
        pageSize: 20,
        search: false,
        pageSizeOptions: [20, 50, 100],
        exportCsv: () => {
          const { url, data } = buildExportAsExcelParams(
            filtering.current,
            ordering
          );
          fetch(url, {
            mode: "cors",
            method: "POST",
            body: JSON.stringify(data),
            headers: {
              "Content-Type": "application/json",
            },
            responseType: "blob",
          })
            .then((response) => response.blob())
            .then((blob) => saveAs(blob, "test.csv"));
        },
      }}
    />
  );
};

export default NFLRushingTable;
