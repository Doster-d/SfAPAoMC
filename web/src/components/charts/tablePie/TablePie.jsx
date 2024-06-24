import ReactApexChart from "react-apexcharts";
import { optionsPie } from "./models";
import { useEffect } from "react";

function TablePie({ series }) {
  const sum = series[0] + series[1] + series[2] + 0.0001;
  useEffect(() => {
    if (window.outerWidth < 1024) {
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
            <th className="charts__table-header">Количество патентов</th>
            <th className="charts__table-header">%</th>
          </tr>
        </thead>
        <tbody>
          <tr className="charts__table-row">
            <td className="charts__table-cell">Юридическое лицо</td>
            <td className="charts__table-cell">{series[0]}</td>
            <td className="charts__table-cell">
              {(series[0] / sum).toFixed(2) * 100}%
            </td>
          </tr>
          <tr className="charts__table-row">
            <td className="charts__table-cell">Инд.предприниматель</td>
            <td className="charts__table-cell">{series[1]}</td>
            <td className="charts__table-cell">
              {(series[1] / sum).toFixed(2) * 100}%
            </td>
          </tr>
          <tr className="charts__table-row">
            <td className="charts__table-cell">Физическое лицо</td>
            <td className="charts__table-cell">{series[2]}</td>
            <td className="charts__table-cell">
              {(series[2] / sum).toFixed(2) * 100}%
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}

export default TablePie;
