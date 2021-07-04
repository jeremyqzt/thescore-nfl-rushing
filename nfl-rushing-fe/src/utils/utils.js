import { SORT_MAP } from "./constants";

export const buildStatsQueryFromParams = (query) => {
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

  return url;
};

export const buildExportAsExcelParams = (filters, ordering) => {
  const data = {
    filter: filters ? filters.value : undefined,
    sort: ordering.orderBy ? SORT_MAP[ordering.orderBy.field] : undefined,
    sort_by: ordering.orderDirection
      ? ordering.orderDirection.toUpperCase()
      : undefined,
  };

  return {
    data,
    url: "http://localhost:8000/api/listStatsExcel/",
  };
};
