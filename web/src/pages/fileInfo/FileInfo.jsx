import { useEffect, useState } from "react";
import "./style.scss";
import MultiRadialBar from "../../components/charts/multiRadialBar/MultiRadialBar";
import SemiRadialBar from "../../components/charts/semiRadialBar/SemiRadialBar";
import TablePie from "../../components/charts/tablePie/TablePie";
import { Helmet } from "react-helmet-async";
import SimplePie from "../../components/charts/simplePie/SimplePie";
import { useParams } from "react-router-dom";
import { useGetFileInfoById } from "./hooks/useGetFileInfoById";
function FileInfo() {
  const { fileId } = useParams();
  const { data: fileData, isPending, isError } = useGetFileInfoById(fileId);
  const [categories, setCategories] = useState([]);
  console.log(fileData);
  useEffect(() => {
    document.body.style =
      "  background:linear-gradient(90deg, rgb(132, 250, 176), rgb(143, 211, 244) 52.465%)";
    return () => {
      document.body.style = "";
    };
  }, []);

  useEffect(() => {
    if (fileData?.data.categories) {
      setCategories(Object.values(fileData?.data.categories));
    }
  }, [fileData]);
  return (
    <>
      <Helmet>
        <title>Файл {fileId}</title>
        <meta name="description" content="Описание определенного файла" />
        <meta rel="canonical" href={`/file/${fileId}`} />
      </Helmet>
      {isPending ? (
        <h2 className="title-h2">Загрузка данных...</h2>
      ) : (
        <main className="file-info">
          <div className="container">
            <h1 className="title-h1 file-info__title">Статистика по файлу</h1>
            <div className="file-info__charts">
              <div className="file-info__charts-row">
                <TablePie
                  series={[
                    fileData?.data.patent_holders.LE,
                    fileData?.data.patent_holders.IE,
                    fileData?.data.patent_holders.PE,
                  ]}
                />
              </div>
              <div className="file-info__charts-row">
                <SimplePie series={categories} />
                <SemiRadialBar
                  series={[
                    Math.round(
                      (
                        fileData?.data.count_found /
                        (fileData?.data.count + 1)
                      ).toFixed(2) * 100
                    ),
                  ]}
                />
              </div>
            </div>
          </div>
        </main>
      )}
    </>
  );
}

export default FileInfo;
