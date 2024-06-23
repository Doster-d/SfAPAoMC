import { Link } from "react-router-dom";
import DownloadBtn from "../../components/downloadBtn/DownloadBtn";
import statBtn from "./../../assets/images/stat.svg";
import moreBtn from "./../../assets/images/more.svg";
import './style.scss'
function FileList() {
  return (
    <main className="file-list">
      <div className="container">
        <h1 className="title-h1 file-list__title">ЗАГРУЖЕННЫЕ ФАЙЛЫ</h1>
        <table className="file-list__table file-table">
          <thead className="file-table__head">
            <tr className="file-table__row">
              <td className="file-table__column">#</td>
              <td className="file-table__column">Наименование файла</td>
              <td className="file-table__column">Дата отправки</td>
              <td className="file-table__column">Пользователь</td>
              <td className="file-table__column">Статистика</td>
              <td className="file-table__column">Скачать</td>
            </tr>
          </thead>
          <tbody>
            <tr className="file-table__row">
              <td className="file-table__column">1</td>
              <td className="file-table__column">FileName</td>
              <td className="file-table__column">Дата</td>
              <td className="file-table__column">Юзернейм</td>
              <td className="file-table__column">
                <Link className="file-table__stat" to={"/file/0"}>
                  Статистика <img src={statBtn} alt="" />
                </Link>
              </td>
              <td className="file-table__column">
                <DownloadBtn fileId={0} />
              </td>
            </tr>
            <tr className="file-table__row">
              <td className="file-table__column">1</td>
              <td className="file-table__column">FileName</td>
              <td className="file-table__column">Дата</td>
              <td className="file-table__column">Юзернейм</td>
              <td className="file-table__column">
                <Link className="file-table__stat" to={"/file/0"}>
                  Статистика <img src={statBtn} alt="" />
                </Link>
              </td>
              <td className="file-table__column">
                <DownloadBtn fileId={0} />
              </td>
            </tr>
            <tr className="file-table__row">
              <td className="file-table__column">1</td>
              <td className="file-table__column">FileName</td>
              <td className="file-table__column">Дата</td>
              <td className="file-table__column">Юзернейм</td>
              <td className="file-table__column">
                <Link className="file-table__stat" to={"/file/0"}>
                  Статистика <img src={statBtn} alt="" />
                </Link>
              </td>
              <td className="file-table__column">
                <DownloadBtn fileId={0} />
              </td>
            </tr>
          </tbody>
        </table>
        <div className="file-table__addition">
          <p className="file-table__number-of-pages">1-5 из n</p>
          <button className="file-table__next-page">Показать еще <img src={moreBtn} alt="" /></button>
        </div>
      </div>
    </main>
  );
}

export default FileList;
