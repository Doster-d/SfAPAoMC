import { useMutation } from "@tanstack/react-query";
import { uploadFile } from "../api/uploadFile";
import { useSelector } from "react-redux";
import { downloadFile } from "../api/downloadFile";
import { useNavigate } from "react-router-dom";


export function useUploadFileMutation(addNotification) {
    const {userId, accessToken} = useSelector((state) => state.user)
    const navigate = useNavigate()
    return useMutation({
        mutationFn: async (data) => (await uploadFile(data, accessToken, userId)),
        onError: (error) => {
            console.log(error);
            addNotification('Что-то пошло не так...', 'bad', 5000)
        },
        onSuccess: async (data) => {
            addNotification(`Файл ${data.data.filename} обработан`, 'good', 3000)
            const response = await downloadFile(accessToken, userId, data.data.fileId)
            navigate(`/file/${data.data.fileId}`)
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const a = document.createElement('a');
            a.href = url;
            a.download = `Обработанный_${data.data.filename}`; // Замените на нужное имя файла и расширение
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url);
            console.log(data);
        }
    })
}