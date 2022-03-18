import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter, Route, Switch } from "react-router-dom";

import "bootstrap/dist/css/bootstrap.css";
import "assets/scss/styles.scss?v=1.3.0";
import "perfect-scrollbar/css/perfect-scrollbar.css";

import AdminLayout from "layouts/Admin.js";
import ResultContextProvider from "context/ResultContext";
import Home from "./views/Home";
import Dashboard from "./views/Dashboard";

ReactDOM.render(
  <ResultContextProvider>
    <BrowserRouter>
      <AdminLayout>
        <Switch>
          <Route path="/dashboard" component={Dashboard} />
          <Route path="/" component={Home} />
        </Switch>
      </AdminLayout>
    </BrowserRouter>
  </ResultContextProvider>,
  document.getElementById("root")
);
