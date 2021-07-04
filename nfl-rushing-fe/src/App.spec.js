import App from "./App";

import React from "react";

import { shallow } from "enzyme";

describe("App", () => {
  it("renders", () => {
    const wrapper = shallow(<App />);
    expect(wrapper.find("NFLRushingTable")).toBeTruthy();
  });
});
