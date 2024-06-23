import "./style.scss";

// Import Swiper styles
import "swiper/css";
import TeamSlider from "../../components/teamSlider/TeamSlider";
import { useEffect, useState } from "react";
import MultiRadialBar from "../../components/charts/multiRadialBar/MultiRadialBar";
import SemiRadialBar from "../../components/charts/semiRadialBar/SemiRadialBar";
import TablePie from "../../components/charts/tablePie/TablePie";
import { Helmet } from "react-helmet-async";
import { useGetGeneralInfo } from "./hooks/useGetGeneralInfo";
import LocalLoader from "../../components/localLoader/LocalLoader";
import { useDispatch } from "react-redux";
import { addNewNotification } from "../../setup/store/reducers/notificationSlice";
import { NOTIFICATION_BAD } from "../../const";
function Mainpage() {
  const { data: generalData, isPending, isError, error } = useGetGeneralInfo();
  const dispatch = useDispatch();
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
    if (isError) {
      dispatch(
        addNewNotification({
          message: "При загрузке общей статистики произошла ошибка",
          NOTIFICATION_BAD,
          duration: 5000,
        })
      );
    }
  }, [isError]);

  return (
    <>
      <Helmet>
        <title>K1 - Анализ патентов</title>
        <meta
          name="description"
          content="Сервис анализа патентной активности компаний Москвы: мониторинг, анализ и визуализация патентов."
        />
        <meta rel="canonical" href="/" />
      </Helmet>
      <main className="main">
        <section className="main-banner">
          <div className="container">
            <h1 className="main-banner__title title-h1">
              Решение кейса “Сервис анализа патентной активности компаний
              Москвы”
            </h1>
          </div>
        </section>
        <TeamSlider />
        <section className="charts">
          <h2 className="title-h2 charts__title">
            {isError ? "ПРОИЗОШЛА ОШИБКА ПРИ ГЕНЕРАЦИИ" : "ОБЩАЯ СТАТИСТИКА"}
          </h2>
          <p className="main-banner__tip">
            Для просмотра дополнительной статистики по каждой категории нажмите на трек
            конкретной категории.
          </p>

          {isPending ? (
            <LocalLoader />
          ) : (
            <div className="container charts__container">
              <div className="charts__main-chart">
                <MultiRadialBar
                  handleBarSelection={handleBarSelection}
                  series={[
                    (
                      generalData?.data?.model?.count /
                      (generalData?.data?.model?.count +
                        generalData?.data?.design?.count +
                        generalData?.data?.invention?.count +
                        0.0001)
                    ).toFixed(2) * 100,
                    (
                      generalData?.data?.design?.count /
                      (generalData?.data?.model?.count +
                        generalData?.data?.design?.count +
                        generalData?.data?.invention?.count +
                        0.0001)
                    ).toFixed(2) * 100,
                    (
                      generalData?.data?.invention?.count /
                      (generalData?.data?.model?.count +
                        generalData?.data?.design?.count +
                        generalData?.data?.invention?.count +
                        0.0001)
                    ).toFixed(2) * 100,
                  ]}
                />
              </div>
              {barSelected && (
                <div className="charts__additional-charts">
                  {barSelected === "Модель" ? (
                    <>
                      <SemiRadialBar
                        series={[
                          (
                            generalData?.data.model.count_found /
                            (generalData?.data.model.count + 0.0001)
                          ).toFixed(2) * 100,
                        ]}
                      />
                      <TablePie
                        series={[
                          generalData?.data.model.patent_holders.LE,
                          generalData?.data.model.patent_holders.IE,
                          generalData?.data.model.patent_holders.PE,
                        ]}
                      />
                    </>
                  ) : barSelected === "Образец" ? (
                    <>
                      <SemiRadialBar
                        series={[
                          (
                            generalData?.data.design.count_found /
                            (generalData?.data.design.count + 0.0001)
                          ).toFixed(2) * 100,
                        ]}
                      />
                      <TablePie
                        series={[
                          generalData?.data.design.patent_holders.LE,
                          generalData?.data.design.patent_holders.IE,
                          generalData?.data.design.patent_holders.PE,
                        ]}
                      />
                    </>
                  ) : (
                    barSelected === "Изобретение" && (
                      <>
                        <SemiRadialBar
                          series={[
                            (
                              generalData?.data.invention.count_found /
                              (generalData?.data.invention.count + 0.0001)
                            ).toFixed(2) * 100,
                          ]}
                        />
                        <TablePie
                          series={[
                            generalData?.data.invention.patent_holders.LE,
                            generalData?.data.invention.patent_holders.IE,
                            generalData?.data.invention.patent_holders.PE,
                          ]}
                        />
                      </>
                    )
                  )}
                </div>
              )}
            </div>
          )}
        </section>
      </main>
    </>
  );
}

export default Mainpage;
