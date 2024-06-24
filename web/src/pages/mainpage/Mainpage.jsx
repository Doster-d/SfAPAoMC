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
import { getCookieByName } from "../../utils";
function Mainpage() {
  const { data: generalData, isPending, isError, error } = useGetGeneralInfo();
  const dispatch = useDispatch();
  const [barSelected, setBarSelected] = useState(undefined);
  const [generalInformation, setGeneralInformation] = useState(
    JSON.parse(getCookieByName("generalInformation"))
  );
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

  useEffect(() => {
    if (generalData) {
      setGeneralInformation(generalData.data);
      const expiresDate = new Date();
      expiresDate.setHours(expiresDate.getHours() + 24);
      document.cookie = `generalInformation=${JSON.stringify(
        generalData.data
      )};expires=${expiresDate.toUTCString()};`;
    }
  }, [generalData]);

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
            Для просмотра дополнительной статистики по каждой категории нажмите
            на трек конкретной категории.
          </p>

          {isPending && Object.keys(generalInformation).length === 0 ? (
            <LocalLoader />
          ) : (
            <div className="container charts__container">
              <div className="charts__main-chart">
                <MultiRadialBar
                  handleBarSelection={handleBarSelection}
                  series={[
                    (
                      generalInformation.model?.count /
                      (generalInformation.model?.count +
                        generalInformation.design?.count +
                        generalInformation.invention?.count +
                        0.0001)
                    ).toFixed(2) * 100,
                    (
                      generalInformation.design?.count /
                      (generalInformation.model?.count +
                        generalInformation.design?.count +
                        generalInformation.invention?.count +
                        0.0001)
                    ).toFixed(2) * 100,
                    (
                      generalInformation.invention?.count /
                      (generalInformation.model?.count +
                        generalInformation.design?.count +
                        generalInformation.invention?.count +
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
                            generalInformation.model.count_found /
                            (generalInformation.model.count + 0.0001)
                          ).toFixed(2) * 100,
                        ]}
                      />
                      <TablePie
                        series={[
                          generalInformation.model.patent_holders.LE,
                          generalInformation.model.patent_holders.IE,
                          generalInformation.model.patent_holders.PE,
                        ]}
                      />
                    </>
                  ) : barSelected === "Образец" ? (
                    <>
                      <SemiRadialBar
                        series={[
                          (
                            generalInformation.design.count_found /
                            (generalInformation.design.count + 0.0001)
                          ).toFixed(2) * 100,
                        ]}
                      />
                      <TablePie
                        series={[
                          generalInformation.design.patent_holders.LE,
                          generalInformation.design.patent_holders.IE,
                          generalInformation.design.patent_holders.PE,
                        ]}
                      />
                    </>
                  ) : (
                    barSelected === "Изобретение" && (
                      <>
                        <SemiRadialBar
                          series={[
                            (
                              generalInformation.invention.count_found /
                              (generalInformation.invention.count + 0.0001)
                            ).toFixed(2) * 100,
                          ]}
                        />
                        <TablePie
                          series={[
                            generalInformation.invention.patent_holders.LE,
                            generalInformation.invention.patent_holders.IE,
                            generalInformation.invention.patent_holders.PE,
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
