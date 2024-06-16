import ReactApexChart from "react-apexcharts";
import { simplePieOptions } from "./models";
import { useEffect } from "react";

function SimplePie({ series }) {
  useEffect(() => {
    if (window.outerWidth < 1024) {
      window.dispatchEvent(new Event("resize"));
    }
  }, []);
  return (
    <ReactApexChart
      options={simplePieOptions}
      series={series}
      type="donut"
      width={460}
    />
  );
}

export default SimplePie;
