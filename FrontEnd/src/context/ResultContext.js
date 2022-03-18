import React, { createContext } from "react";
import axios from "axios";

export const ResultContext = createContext();

class ResultContextProvider extends React.Component {
  state = {
    result: "",
    flux_a: [],
    flux_b: [],
    flux_c: [],
    flux_x: [],
    flux_m: [],
    comb: [],
  };

  process = (result) => {
    const lines = result.split("\n");
    const obj = {
      flux_a: [],
      flux_b: [],
      flux_c: [],
      flux_m: [],
      flux_x: [],
      comb: [],
    };
    const fluxes = ["flux_a", "flux_b", "flux_c", "flux_x", "flux_m"];
    for (let i = 1; i < lines.length; i++) {
      const words = lines[i].split(",");
      const type = words[0][words[0].length - 1].toLowerCase();
      const combFlux1 = {},
        combFlux2 = {},
        combFlux3 = {};
      for (let ind in fluxes) {
        if (fluxes[ind] === "flux_" + type) {
          combFlux1.time = parseFloat(words[1]);
          combFlux1[fluxes[ind]] = parseFloat(words[5]);
          obj[fluxes[ind]].push({
            time: combFlux1.time,
            [fluxes[ind]]: combFlux1[fluxes[ind]],
            status: "Rise Point",
          });

          combFlux2.time = parseFloat(words[2]);
          combFlux2[fluxes[ind]] = parseFloat(words[4]);
          obj[fluxes[ind]].push({
            time: combFlux2.time,
            [fluxes[ind]]: combFlux2[fluxes[ind]],
            status: "Peak Point",
            "rise-time": new Date(parseFloat(words[1])).toLocaleString(),
            "peak-time": new Date(parseFloat(words[2])).toLocaleString(),
            "decay-time": new Date(parseFloat(words[3])).toLocaleString(),
            "peak-flux": parseFloat(words[4]),
            bg_for_the_peak_flux: parseFloat(words[5]),
            type: words[0],
          });

          combFlux3.time = parseFloat(words[3]);
          combFlux3[fluxes[ind]] = parseFloat(words[5]);
          obj[fluxes[ind]].push({
            time: combFlux3.time,
            [fluxes[ind]]: combFlux3[fluxes[ind]],
            status: "Decay Point",
          });
        } else {
          combFlux1[fluxes[ind]] = 0;
          obj[fluxes[ind]].push({
            time: new Date(parseFloat(words[1])).getTime(),
            [fluxes[ind]]: 0,
          });

          combFlux2[fluxes[ind]] = 0;
          obj[fluxes[ind]].push({
            time: new Date(parseFloat(words[2])).getTime(),
            [fluxes[ind]]: 0,
          });

          combFlux3[fluxes[ind]] = 0;
          obj[fluxes[ind]].push({
            time: new Date(parseFloat(words[3])).getTime(),
            [fluxes[ind]]: 0,
          });
        }
      }
      obj.comb.push(combFlux1, combFlux2, combFlux3);
    }

    this.setState({
      result,
      ...obj,
    });
  };

  async componentDidMount() {
    try {
      const result = await axios.get("http://localhost:3000/result/");
      // console.log("Result", result);
      this.process(result.data);
    } catch (err) {
      console.log("Error while fetching result from the backend", err.message);
      if (err.response) {
        alert(err.response.data);
      }
    }
  }

  render() {
    return (
      <ResultContext.Provider value={{ ...this.state, process: this.process }}>
        {this.state.result === "" ? <></> : this.props.children}
      </ResultContext.Provider>
    );
  }
}

export default ResultContextProvider;
