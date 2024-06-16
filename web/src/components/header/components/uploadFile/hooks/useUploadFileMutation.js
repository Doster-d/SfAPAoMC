import { useMutation } from "@tanstack/react-query";
import { uploadFile } from "../api/uploadFile";
import { useSelector } from "react-redux";


export function useUploadFileMutation(addNotification) {
    const {userId, accessToken} = useSelector((state) => state.user)
    return useMutation({
        mutationFn: async (data) => (await uploadFile(data, accessToken, userId)),
        onError: (error) => {
            console.log(error);
            addNotification('Что-то пошло не так...', 'bad', 5000)
        },
        onSuccess: (data) => {
            console.log(data);
        }
    })
}