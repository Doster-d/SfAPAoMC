import ReactApexChart from "react-apexcharts";
import { getOptionsMultiRadial } from "./models";
import "./../style.scss";
function MultiRadialBar({ handleBarSelection, series }) {
  const optionsMultiRadial = getOptionsMultiRadial(handleBarSelection);
  return (
    <ReactApexChart
      options={optionsMultiRadial}
      series={series}
      type="radialBar"
      height={502}
    />
  );
}

export default MultiRadialBar;
