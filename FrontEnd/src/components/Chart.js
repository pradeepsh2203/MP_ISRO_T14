import {
  LineChart,
  ResponsiveContainer,
  Legend,
  Tooltip,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
} from "recharts";
import React from "react";

const Chart = ({ data, chartType }) => {
  return (
    <div>
      <ResponsiveContainer width="100%" aspect={3}>
        <LineChart
          data={data}
          margin={{ top: 5, right: 40, left: 20, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            label={{
              value: "Time",
              position: "insideBottom",
            }}
            dataKey="time"
            tickFormatter={(time) => {
              return new Date(time).toLocaleString("en-US", {
                hour: "numeric",
                minute: "2-digit",
                second: "numeric",
                // dateStyle: "short",
              });
            }}
            domain={["dataMin", "dataMax"]}
            type="number"
            scale="time"
          />
          <YAxis
            label={{ value: "Flux" }}
            tick={false}
            domain={["0", "dataMax"]}
          />
          <Tooltip
            // labelFormatter={(value) =>
            // 	new Date(value).toLocaleString("en-US", {
            // 		day: "numeric",
            // 		year: "numeric",
            // 		month: "short",
            // 		hour: "numeric",
            // 		minute: "2-digit",
            // 		second: "2-digit",
            // 	})
            // }
            content={<CustomToolTip />}
          />
          {chartType === "" && (
            <Legend
              layout="vertical"
              verticalAlign="top"
              align="right"
              wrapperStyle={{ right: "0" }}
            />
          )}
          {(chartType === "Type A" || chartType === "") && (
            <Line
              type="monotone"
              label="Type A"
              dataKey="flux_a"
              stroke="#6bd098"
              dot={false}
            />
          )}
          {(chartType === "Type B" || chartType === "") && (
            <Line
              type="monotone"
              dataKey="flux_b"
              stroke="#f17e5d"
              dot={false}
            />
          )}
          {(chartType === "Type C" || chartType === "") && (
            <Line
              type="monotone"
              dataKey="flux_c"
              stroke="#fcc468"
              dot={false}
            />
          )}
          {(chartType === "Type X" || chartType === "") && (
            <Line
              type="monotone"
              dataKey="flux_x"
              stroke="#d296da"
              dot={false}
            />
          )}
          {(chartType === "Type M" || chartType === "") && (
            <Line
              type="monotone"
              dataKey="flux_m"
              stroke="#72b3b3"
              dot={false}
            />
          )}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

const CustomToolTip = ({ active, payload, label }) => {
  // console.log(payload, label);
  const data = payload;
  if (active && data && label) {
    return (
      <div className="custom-tooltip bg-primary rounded text-light p-2">
        <p className="label font-weight-bold">
          {new Date(label).toLocaleString("en-US", {
            day: "numeric",
            year: "numeric",
            month: "short",
            hour: "numeric",
            minute: "2-digit",
            second: "2-digit",
          })}
        </p>
        {data.map((d, ind) => (
          <div key={ind}>
            <p className="Info">
              {d.dataKey} : {d.value}
            </p>
            {d.payload.status === "Peak Point" && (
              <>
                <p className="Info">Rise Time : {d.payload["rise-time"]}</p>
                <p className="Info">Peak Time : {d.payload["peak-time"]}</p>
                <p className="Info">Decay Time : {d.payload["decay-time"]}</p>
                <p className="Info">Peak Flux : {d.payload["peak-flux"]}</p>
                <p className="Info">
                  Background Flux : {d.payload.bg_for_the_peak_flux}
                </p>
                <p className="Info">Type : {d.payload.type}</p>
              </>
            )}
          </div>
        ))}
      </div>
    );
  }
  return null;
};

export default Chart;
