import { buildStatsQueryFromParams, buildExportAsExcelParams } from "./utils";

describe("Utils", () => {
  it("buildStatsQueryFromParams", () => {
    const query = {
      page_size: 10,
      page: 1,
      filters: [{ value: "test" }],
      orderBy: { field: "test2" },
      orderDirection: "asc",
    };

    const expected =
      "http://localhost:8000/api/listStats?page_size=undefined&page=2&filter=test&sort=undefined&sort_by=ASC";

    const url = buildStatsQueryFromParams(query);
    expect(url).toEqual(expected);
  });

  it("buildExportAsExcelParams", () => {
    const sort = {
      orderBy: {
        field: "Lng",
      },
      orderDirection: "ASC",
    };

    const filter = {
      value: "test",
    };

    const expected = {
      data: { filter: "test", sort: "LONGEST_RUSH", sort_by: "ASC" },
      url: "http://localhost:8000/api/listStatsExcel/",
    };

    const query = buildExportAsExcelParams(filter, sort);
    expect(query).toEqual(expected);
  });
});
