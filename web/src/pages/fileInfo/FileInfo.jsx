import { useEffect, useState } from "react";
import "./style.scss";
import MultiRadialBar from "../../components/charts/multiRadialBar/MultiRadialBar";
import SemiRadialBar from "../../components/charts/semiRadialBar/SemiRadialBar";
import TablePie from "../../components/charts/tablePie/TablePie";
import ReactApexChart from "react-apexcharts";
import SimplePie from "../../components/charts/simplePie/SimplePie";
function FileInfo() {
  const [barSelected, setBarSelected] = useState(undefined);
  useEffect(() => {
    console.log(barSelected);
  }, [barSelected]);
  const handleBarSelection = (event) => {
    if (event.target.parentElement.attributes.seriesName) {
      if (event.target.attributes.selected.value === "true") {
        setBarSelected(event.target.parentElement.attributes.seriesName.value);
      } else {
        setBarSelected(undefined);
      }
    }
  };
  useEffect(() => {
    document.body.style =
      "  background:linear-gradient(90deg, rgb(132, 250, 176), rgb(143, 211, 244) 52.465%)";
    return () => {
      document.body.style = "";
    };
  }, []);

  
  return (
    <main className="file-info">
      <div className="container">
        <h1 className="title-h1 file-info__title">
          Статистика по файлу “наименование_файла”
        </h1>
        <div className="file-info__charts">
          <div className="file-info__charts-row">
            <MultiRadialBar
              handleBarSelection={handleBarSelection}
              series={[100, 90, 80]}
            />
            <TablePie series={[28, 12, 6]} />
          </div>
          <div className="file-info__charts-row">
            <SimplePie series={[44, 55, 17, 15]}/>
            <SemiRadialBar series={[72]} />
          </div>
        </div>
      </div>
    </main>
  );
}

export default FileInfo;
