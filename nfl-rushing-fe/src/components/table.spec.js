import React from "react";

import NFLRushingTable from "./table";
import { shallow, mount } from "enzyme";
import { columns } from "../utils/constants";

global.fetch = jest.fn(() =>
  Promise.resolve({
    json: () => Promise.resolve({}),
  })
);

describe("NFLRushingTable", () => {
  beforeEach(() => {
    fetch.mockClear();
  });

  it("renders", () => {
    const wrapper = shallow(<NFLRushingTable />);
    expect(wrapper).toBeTruthy();
  });

  it("renders columns", () => {
    const wrapper = mount(<NFLRushingTable />);
    const renderColumns = wrapper.find("MaterialTable").prop("columns");
    renderColumns.forEach((column) => {
      expect(
        columns.some((actualColumn) => actualColumn.field === column.field)
      ).toBeTruthy();
    });
  });

  it("calls fetch for data", async () => {
    mount(<NFLRushingTable />);
    expect(fetch).toHaveBeenCalledTimes(1);
  });
});
