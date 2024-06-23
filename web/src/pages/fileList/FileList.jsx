import DownloadBtn from "../../components/downloadBtn/DownloadBtn";

function FileList() {
  return (
    <main className="file-list">
      <div className="container">
        <h1 className="title-h1">ЗАГРУЖЕННЫЕ ФАЙЛЫ</h1>
        <table className="file-list__table file-table">
            <thead className="file-table__head">
                <td className="file-table__column">#</td>
                <td className="file-table__column">Наименование файла</td>
                <td className="file-table__column">Дата отправки</td>
                <td className="file-table__column">Пользователь</td>
                <td className="file-table__column">Статистика</td>
                <td className="file-table__column">Скачать</td>
            </thead>
            <tbody>
              <tr className="file-table__row">
                <td className="file-table__column">1</td>
                <td className="file-table__column">FileName</td>
                <td className="file-table__column">Дата</td>
                <td className="file-table__column">Юзернейм</td>
                <td className="file-table__column"></td>
                <td className="file-table__column"><DownloadBtn fileId={0}/></td>
              </tr>
            </tbody>
        </table>
      </div>
    </main>
  );
}

export default FileList;
