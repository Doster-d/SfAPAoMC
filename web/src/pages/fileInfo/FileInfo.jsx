import { useEffect, useState } from "react";
import "./style.scss";
import MultiRadialBar from "../../components/charts/multiRadialBar/MultiRadialBar";
import SemiRadialBar from "../../components/charts/semiRadialBar/SemiRadialBar";
import TablePie from "../../components/charts/tablePie/TablePie";
import { Helmet } from "react-helmet-async";
import SimplePie from "../../components/charts/simplePie/SimplePie";
import { useParams } from "react-router-dom";
function FileInfo() {
  const {fileId} = useParams();
  const [barSelected, setBarSelected] = useState(undefined);
  useEffect(() => {
    document.body.style =
      "  background:linear-gradient(90deg, rgb(132, 250, 176), rgb(143, 211, 244) 52.465%)";
    return () => {
      document.body.style = "";
    };
  }, []);


  const handleBarSelection = (event) => {
    if (
      event.target.parentElement.attributes.seriesName ||
      event.target.attributes.selected
    ) {
      if (event.target.attributes.selected?.value === "true") {
        setBarSelected(event.target.parentElement.attributes.seriesName?.value);
      } else {
        setBarSelected(undefined);
      }
    }
  };

  return (
    <>
      <Helmet>
        <title>Файл {fileId}</title>
        <meta
          name="description"
          content="Описание определенного файла"
        />
        <meta rel="canonical" href={`/file/${fileId}`} />
      </Helmet>
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
              <SimplePie series={[44, 55, 17, 15]} />
              <SemiRadialBar series={[72]} />
            </div>
          </div>
        </div>
      </main>
    </>
  );
}

export default FileInfo;
