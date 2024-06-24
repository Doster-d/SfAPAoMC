import { Link } from "react-router-dom";
import DownloadBtn from "../../components/downloadBtn/DownloadBtn";
import statBtn from "./../../assets/images/stat.svg";
import moreBtn from "./../../assets/images/more.svg";
import "./style.scss";
import { useGetFiles } from "./hooks/useGetFiles";
import { Fragment, useState } from "react";
import GlobalLoader from "../../components/globalLoader/GlobalLoader";
function FileList() {
  const [filesCounter, setFilesCounter] = useState(1);
  const filesQuery = useGetFiles();
  if (filesQuery.isFetching) {
    return <GlobalLoader />;
  }
  console.log(filesQuery.data);
  return (
    <main className="file-list">
      <div className="container file-list__container">
        <h1 className="title-h1 file-list__title">ЗАГРУЖЕННЫЕ ФАЙЛЫ</h1>
        <div className="file-list__table-wrapper">
          <table className="file-list__table file-table">
            <thead className="file-table__head">
              <tr className="file-table__row">
                <td className="file-table__column">id</td>
                <td className="file-table__column">Наименование файла</td>
                <td className="file-table__column">Пользователь</td>
                <td className="file-table__column">Статистика</td>
                <td className="file-table__column">Скачать</td>
              </tr>
            </thead>
            <tbody>
              {filesQuery.data?.pages.map((group, index) => {
                console.log(group);
                return (
                  <Fragment key={index}>
                    {group?.filesInfo.map((file) => (
                      <tr className="file-table__row">
                        <td className="file-table__column">{file.id}</td>
                        <td className="file-table__column">{file.fileName}</td>
                        <td className="file-table__column">
                          {file.authorName}
                        </td>
                        <td className="file-table__column">
                          <Link
                            className="file-table__stat"
                            to={`/file/${file.id}`}
                          >
                            Статистика <img src={statBtn} alt="" />
                          </Link>
                        </td>
                        <td className="file-table__column">
                          <DownloadBtn fileId={file.id} />
                        </td>
                      </tr>
                    ))}
                  </Fragment>
                );
              })}
            </tbody>
          </table>
        </div>
        <div className="file-table__addition">
          {filesQuery.hasNextPage && (
            <button
              disabled={filesQuery.isFetchingNextPage}
              onClick={() => filesQuery.fetchNextPage()}
              className="file-table__next-page"
            >
              {filesQuery.isFetchingNextPage ? "Загрузка..." : "Показать еще"}{" "}
              <img src={moreBtn} alt="" />
            </button>
          )}
        </div>
      </div>
    </main>
  );
}

export default FileList;
