import ReactApexChart from "react-apexcharts";
import { optionsSemiRadial } from "./models";
import { useEffect } from "react";

function SemiRadialBar({ series }) {
  useEffect(() => {
    if(window.outerWidth < 1024) {
      window.dispatchEvent(new Event("resize"));
    }
  }, []);
  return (
    <ReactApexChart
      options={optionsSemiRadial}
      series={series}
      type="radialBar"
      height={"502px"}
      width={502}
    />
  );
}

export default SemiRadialBar;
