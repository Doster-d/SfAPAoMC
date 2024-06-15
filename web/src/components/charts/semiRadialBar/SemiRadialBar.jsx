import ReactApexChart from "react-apexcharts";
import { optionsSemiRadial } from "./models";

function SemiRadialBar({series}) {
  return (
    <ReactApexChart
      options={optionsSemiRadial}
      series={series}
      type="radialBar"
      height={502}
      width={502}
    />
  );
}

export default SemiRadialBar;
