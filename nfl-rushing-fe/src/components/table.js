import { useState } from "react";
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
  const [filters, setFilters] = useState({});
  const [ordering, setOrdering] = useState({});

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

  const RENDER_COLUMNS = columns.map((column) => {
    if (FILTERABLE_COLUMNS.includes(column.field)) {
      return {
        ...column,
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
              console.log(result);
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
              setFilters({
                filter: value,
              });
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
          const { url, data } = buildExportAsExcelParams(filters, ordering);

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
