import { useState } from "react";
import "./style.scss";
function UploadFile({addNotification}) {
  const [drop, setDrop] = useState(false);

  const [fileName, setFileName] = useState(undefined)
  const handleFile = (file) => {
    console.log(file);
    if(file.type !== 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet') {
        addNotification("Не правильный тип файла", 'bad', 5000)
        return;
    }
    addNotification("Файл добавлен", 'good', 5000)
    setFileName(file.name)
  };
  const onDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();

    setDrop(false);
  };

  const onDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDrop(true);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const droppedFile = e.dataTransfer.files[0];
    setDrop(false);

    handleFile(droppedFile);
  };
  const handleFileChange = (e) => {
    e.preventDefault();
    setDrop(false);

    console.log(e);
    handleFile(e.target.files[0])
  }
  return (
    <form
      className="upload-form"
      onDrop={handleDrop}
      onDragOver={onDragOver}
      onDragLeave={onDragLeave}
    >
      <label
        htmlFor="upload-input"
        className={
          drop
            ? "upload-form__label upload-form__label--dropping"
            : "upload-form__label"
        }
      >
        {!drop && (
          <>
            <span className="upload-form__span">{fileName ? 'Файл загружен' : 'Загузить файлы'}</span>
            <input
              id="upload-input"
              className="upload-form__input"
              type="file"
              onChange={handleFileChange}
              accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            />
            <span className="upload-form__add-span">{fileName ? fileName : 'Формат .xlxs'}</span>
          </>
        )}
      </label>
    </form>
  );
}

export default UploadFile;
