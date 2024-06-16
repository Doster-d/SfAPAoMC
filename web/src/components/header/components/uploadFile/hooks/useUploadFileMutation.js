import { useMutation } from "@tanstack/react-query";
import { uploadFile } from "../api/uploadFile";


export function useUploadFileMutation(addNotification) {
    return useMutation({
        mutationFn: async () => (await uploadFile(data)),
        onError: (error) => {
            console.log(error);
            addNotification('Что-то пошло не так...', 'bad', 5000)
        },
        onSuccess: (data) => {
            console.log(data);
        }
    })
}