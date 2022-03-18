import React from "react";
import Dropzone from "../components/Dropzone";
// reactstrap components
import { Card, CardBody, CardImg, Row, Col } from "reactstrap";

function Home() {
  return (
    <>
      <div className="content">
        <Row>
          <Col md="12">
            <Card className="text-center">
              <CardBody>
                Solar flares go through several stages, and there is no accurate
                way to forecast their strength or duration. Each of these stages
                might last anywhere from a few seconds and an hour. Here, we
                develop an automated flare detection algorithm that allows us to
                analyze the time series data of light curve.
              </CardBody>
            </Card>
          </Col>
        </Row>
        <h3 className="text-center">Further Reading</h3>
        <Row>
          <Col md="4">
            <a href="https://en.wikipedia.org/wiki/Solar_flare">
              <Card className="text-center">
                <CardImg
                  top
                  style={{ height: 300, objectFit: "cover" }}
                  src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/X_Class_Solar_Flare_Sends_%E2%80%98Shockwaves%E2%80%99_on_The_Sun_%286819094556%29.jpg/330px-X_Class_Solar_Flare_Sends_%E2%80%98Shockwaves%E2%80%99_on_The_Sun_%286819094556%29.jpg"
                  alt="link to article"
                />
                <CardBody>
                  An X5.4-class solar flare as seen in 131 Å on 6 March 2012.
                  The flare appears as a bright point in the center of the
                  image.
                </CardBody>
              </Card>
            </a>
          </Col>
          <Col md="4">
            <a href="https://www.esa.int/Science_Exploration/Space_Science/What_are_solar_flares">
              <Card className="text-center">
                <CardImg
                  top
                  style={{ height: 300, objectFit: "cover" }}
                  src="https://www.esa.int/var/esa/storage/images/esa_multimedia/images/2000/09/a_solar_eruption/9230577-5-eng-GB/A_solar_eruption_article.jpg"
                  alt="link to article"
                />
                <CardBody>
                  A solar flare is a tremendous explosion on the Sun that
                  happens when energy stored in 'twisted' magnetic fields
                  (usually above sunspots) is suddenly released.
                </CardBody>
              </Card>
            </a>
          </Col>
          <Col md="4">
            <a href="https://www.nsf.gov/discoveries/disc_summ.jsp?cntn_id=299753">
              <Card className="text-center">
                <CardImg
                  top
                  style={{ height: 300, objectFit: "cover" }}
                  src="https://www.nsf.gov/news/mmg/media/images/RN-solar-flares_f.jpg"
                  alt="link to article"
                />
                <CardBody>
                  The imager on the GOES-R series satellites collects data
                  corresponding to different temperatures.
                </CardBody>
              </Card>
            </a>
          </Col>
        </Row>
        <h3 className="text-center">How to use</h3>
        <Row>
          <Col md="12">
            <Card className="text-center">
              <CardBody>
                <Dropzone />
              </CardBody>
            </Card>
          </Col>
        </Row>
        <Col md="12">
          <Card className="text-center">
            <CardBody>
              A light curve is a graph that depicts an object's brightness over
              time. The light curve is a basic but important tool for scientists
              studying objects that alter their brightness over time, such as
              novae, supernovae, and variable stars. A light curve's record of
              variations can aid an astronomer in comprehending both the
              mechanisms at work and in identifying certain types of stellar
              occurrences.
            </CardBody>
          </Card>
        </Col>
      </div>
    </>
  );
}

export default Home;
