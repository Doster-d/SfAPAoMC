import downloadBtn from "./../../assets/images/download_btn.svg";
import { useDownloadFile } from "./hooks/useDownloadFile";
import './style.scss'
function DownloadBtn({ fileId }) {
  const downloadFileMutation = useDownloadFile();
  const handleClick = async () => {
    const response = await downloadFileMutation.mutateAsync(fileId);
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const a = document.createElement("a");
    a.href = url;
    a.download = `Обработанный_${data.data.filename}`; // Замените на нужное имя файла и расширение
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
  };
  return (
    <button
      disabled={downloadFileMutation.isPending}
      onClick={handleClick}
      className="download-btn"
    >
      {downloadFileMutation.isPending ? "Скачиваем..." : "Скачать"}{" "}
      <img src={downloadBtn} alt="" />
    </button>
  );
}

export default DownloadBtn;
