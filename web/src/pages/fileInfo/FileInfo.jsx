import { useEffect, useState } from "react";
import "./style.scss";
import MultiRadialBar from "../../components/charts/multiRadialBar/MultiRadialBar";
import SemiRadialBar from "../../components/charts/semiRadialBar/SemiRadialBar";
import TablePie from "../../components/charts/tablePie/TablePie";
import { Helmet } from "react-helmet-async";
import SimplePie from "../../components/charts/simplePie/SimplePie";
import { useNavigate, useParams } from "react-router-dom";
import { useGetFileInfoById } from "./hooks/useGetFileInfoById";
import GlobalLoader from "../../components/globalLoader/GlobalLoader";
import { useDispatch } from "react-redux";
import { addNewNotification } from "../../setup/store/reducers/notificationSlice";
import { NOTIFICATION_BAD } from "../../const";
import DownloadBtn from "../../components/downloadBtn/DownloadBtn";
function FileInfo() {
  const { fileId } = useParams();
  const { data: fileData, isPending, isError } = useGetFileInfoById(fileId);
  const [categories, setCategories] = useState([]);
  const dispatch = useDispatch();
  const navigate = useNavigate();
  console.log(fileData);
  const [barSelected, setBarSelected] = useState(undefined);

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
  useEffect(() => {
    document.body.style =
      "  background:linear-gradient(90deg, rgb(132, 250, 176), rgb(143, 211, 244) 52.465%)";
    return () => {
      document.body.style = "";
    };
  }, []);

  useEffect(() => {
    if (fileData?.data.classificationData.general_classification) {
      setCategories(Object.values(fileData?.data.categories));
    }
  }, [fileData]);
  useEffect(() => {
    if (isError) {
      dispatch(
        addNewNotification({
          message: "При загрузке данных по файлу произошла ошибка",
          type: NOTIFICATION_BAD,
          duration: 5000,
        })
      );
      /* TO-DO  УБРАТЬ КОММЕНТАРИЙ В ПРОДЕ*/
      //navigate('/')
    }
  }, [isError]);
  return (
    <>
      <Helmet>
        <title>Файл {fileId}</title>
        <meta name="description" content="Описание определенного файла" />
        <meta rel="canonical" href={`/file/${fileId}`} />
      </Helmet>
      {isPending ? (
        <GlobalLoader />
      ) : (
        <main className="file-info">
          <div className="container">
            <div className="file-info__upper">
              <h1 className="title-h1 file-info__title">Статистика по файлу</h1>
              <DownloadBtn fileId={fileId} />
            </div>
            <p className="file-info__author">
              Автор — {fileData?.data?.authorUsername}
            </p>
            <p className="file-info__name">
              Наименование файла — {fileData?.data?.fileName}
            </p>
            <div className="file-info__charts">
              <div className="file-info__charts-row">
                <MultiRadialBar
                  series={[
                    Math.round(
                      (
                        fileData?.data.classificationData.model?.count /
                        (fileData?.data.classificationData.model?.count +
                          fileData?.data.classificationData.design?.count +
                          fileData?.data.classificationData.invention?.count +
                          0.0001)
                      ).toFixed(2) * 100
                    ),
                    Math.round(
                      (
                        fileData?.data.classificationData.design?.count /
                        (fileData?.data.classificationData.model?.count +
                          fileData?.data.classificationData.design?.count +
                          fileData?.data.classificationData.invention?.count +
                          0.0001)
                      ).toFixed(2) * 100
                    ),
                    Math.round(
                      (
                        fileData?.data.classificationData.invention?.count /
                        (fileData?.data.classificationData.model?.count +
                          fileData?.data.classificationData.design?.count +
                          fileData?.data.classificationData.invention?.count +
                          0.0001)
                      ).toFixed(2) * 100
                    ),
                  ]}
                  handleBarSelection={handleBarSelection}
                />
                {barSelected === "Модель" ? (
                  <TablePie
                    series={[
                      fileData?.data.classificationData.model.patent_holders.LE,
                      fileData?.data.classificationData.model.patent_holders.IE,
                      fileData?.data.classificationData.model.patent_holders.PE,
                    ]}
                  />
                ) : barSelected === "Образец" ? (
                  <TablePie
                    series={[
                      fileData?.data.classificationData.design.patent_holders
                        .LE,
                      fileData?.data.classificationData.design.patent_holders
                        .IE,
                      fileData?.data.classificationData.design.patent_holders
                        .PE,
                    ]}
                  />
                ) : (
                  barSelected === "Изобретение" && (
                    <TablePie
                      series={[
                        fileData?.data.classificationData.invention
                          .patent_holders.LE,
                        fileData?.data.classificationData.invention
                          .patent_holders.IE,
                        fileData?.data.classificationData.invention
                          .patent_holders.PE,
                      ]}
                    />
                  )
                )}
              </div>
              <div className="file-info__charts-row">
                <SimplePie series={categories} />
                {barSelected === "Модель" ? (
                  <SemiRadialBar
                    series={[
                      Math.round(
                        (
                          fileData?.data.classificationData.model?.count_found /
                          (fileData?.data.classificationData.model?.count +
                            0.0001)
                        ).toFixed(2) * 100
                      ),
                    ]}
                  />
                ) : barSelected === "Образец" ? (
                  <SemiRadialBar
                    series={[
                      Math.round(
                        (
                          fileData?.data.classificationData.design
                            ?.count_found /
                          (fileData?.data.classificationData.design?.count +
                            0.0001)
                        ).toFixed(2) * 100
                      ),
                    ]}
                  />
                ) : (
                  barSelected === "Изобретение" && (
                    <SemiRadialBar
                      series={[
                        Math.round(
                          (
                            fileData?.data.classificationData.invention
                              ?.count_found /
                            (fileData?.data.classificationData.invention
                              ?.count +
                              0.0001)
                          ).toFixed(2) * 100
                        ),
                      ]}
                    />
                  )
                )}
              </div>
            </div>
          </div>
        </main>
      )}
    </>
  );
}

export default FileInfo;
