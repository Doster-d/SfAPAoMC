import ReactApexChart from "react-apexcharts";
import { optionsPie } from "./models";
import { useEffect } from "react";

function TablePie({ series }) {
  useEffect(() => {
    if(window.outerWidth < 1024) {
      window.dispatchEvent(new Event("resize"));
    }
  }, []);
  return (
    <div className="charts__table-pie">
      <ReactApexChart
        options={optionsPie}
        series={series}
        type="donut"
        width={397}
      />
      <table className="charts__table">
        <thead>
          <tr className="charts__table-row">
            <th className="charts__table-header">Тип правообладателя</th>
            <th className="charts__table-header">Количество</th>
            <th className="charts__table-header">%</th>
          </tr>
        </thead>
        <tbody>
          <tr className="charts__table-row">
            <td className="charts__table-cell">Юридическое лицо</td>
            <td className="charts__table-cell">28</td>
            <td className="charts__table-cell">62.5%</td>
          </tr>
          <tr className="charts__table-row">
            <td className="charts__table-cell">Инд.предприниматель</td>
            <td className="charts__table-cell">12</td>
            <td className="charts__table-cell">25%</td>
          </tr>
          <tr className="charts__table-row">
            <td className="charts__table-cell">Физическое лицо</td>
            <td className="charts__table-cell">6</td>
            <td className="charts__table-cell">12.5%</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}

export default TablePie;
