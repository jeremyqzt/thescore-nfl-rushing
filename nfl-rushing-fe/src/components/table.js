import { useState } from "react";
import MaterialTable, { MTableBody } from "material-table";
import {
  tableIcons,
  columns,
  SORTABLE_COLUMNS,
  FILTERABLE_COLUMNS,
  SORT_MAP,
} from "../utils/constants";
import { saveAs } from "file-saver";

const NFLRushingTable = () => {
  const [filters, setFilters] = useState({});
  const [ordering, setOrdering] = useState({});

  const renderColumns = columns.map((column) => {
    if (FILTERABLE_COLUMNS.includes(column.field)) {
      return {
        ...column,
        sorting: false,
        customFilterAndSearch: (term, rowData) => term == rowData.name.length,
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
      columns={renderColumns}
      data={(query) =>
        new Promise((resolve, _) => {
          let url = "http://localhost:8000/api/listStats?";
          url += `page_size=${query.pageSize}`;
          url += `&page=${query.page + 1}`;
          if (query.filters.length > 0) {
            url += `&filter=${query.filters[0].value}`;
          }

          if (query.orderBy && query.orderDirection) {
            url += `&sort=${
              SORT_MAP[query.orderBy.field]
            }&sort_by=${query.orderDirection.toUpperCase()}`;
          }

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
      onOrderChange={(order, direction) => {
        if (order !== -1) {
          setOrdering({
            orderBy: { field: renderColumns[order].field },
            orderDirection: direction,
          });
        } else {
          setOrdering({});
        }
      }}
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
        pageSize: 10,
        search: false,
        pageSizeOptions: [10, 20, 50],
        exportCsv: () => {
          let url = "http://localhost:8000/api/listStatsExcel/";

          const data = {
            filter: filters ? filters.value : undefined,
            sort: ordering.orderBy
              ? SORT_MAP[ordering.orderBy.field]
              : undefined,
            sort_by: ordering.orderDirection
              ? ordering.orderDirection.toUpperCase()
              : undefined,
          };

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
