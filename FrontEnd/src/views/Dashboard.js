import React from "react";
// react plugin used to create charts
// reactstrap components
import {
  Card,
  CardHeader,
  CardBody,
  CardTitle,
  Row,
  Col,
  Button,
} from "reactstrap";
// core components
import WithFluxData from "hoc/WithFluxData";
import Chart from "../components/Chart";
import { useState } from "react";
import Piechart from "components/PieChart";

function Dashboard({ masterChart, AChart, BChart, CChart, XChart, MChart }) {
  const types = ["Type A", "Type B", "Type C", "Type X", "Type M"];
  const [type, setType] = useState("Type A");
  let data;
  if (type === "Type A") data = AChart;
  else if (type === "Type B") data = BChart;
  else if (type === "Type C") data = CChart;
  else if (type === "Type X") data = XChart;
  else data = MChart;
  return (
    <>
      <div className="content">
        <Row>
          <Col md="12">
            <Card>
              <CardHeader>
                <CardTitle tag="h5">Flux</CardTitle>
                <p className="card-category">24 Hours flux</p>
              </CardHeader>
              <CardBody>
                <Chart data={masterChart} chartType=""></Chart>
              </CardBody>
            </Card>
          </Col>
        </Row>
        <Row>
          <Col md="4">
            <Card>
              <CardHeader>
                <CardTitle tag="h5">Flare classification statistics</CardTitle>
              </CardHeader>
              <CardBody style={{ height: "266px" }}>
                <Piechart />
              </CardBody>
            </Card>
          </Col>
          <Col md="8">
            <Card className="card-chart">
              <CardHeader>
                <CardTitle tag="h5">Flare distribution</CardTitle>
                {types.map((t) => (
                  <Button
                    color="primary"
                    outline={t !== type}
                    onClick={() => setType(t)}
                  >
                    {t}
                  </Button>
                ))}
              </CardHeader>
              <CardBody>
                <Chart data={data} chartType={type} />
              </CardBody>
            </Card>
          </Col>
        </Row>
        <img src="http://localhost:3000/static/file34.png" alt="image" />
      </div>
    </>
  );
}

export default WithFluxData(Dashboard);
