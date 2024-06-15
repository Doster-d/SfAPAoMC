import ReactApexChart from "react-apexcharts";
import { getOptionsMultiRadial } from "./models";
import "./../style.scss";
import { useEffect } from "react";
function MultiRadialBar({ handleBarSelection, series }) {
  const optionsMultiRadial = getOptionsMultiRadial(handleBarSelection);
  useEffect(() => {
    if(window.outerWidth < 1024) {
      window.dispatchEvent(new Event("resize"));
    }
  }, []);
  return (
    <ReactApexChart
      options={optionsMultiRadial}
      series={series}
      type="radialBar"
      height={502}
      width={502}
    />
  );
}

export default MultiRadialBar;
