import { useQuery } from "@tanstack/react-query";
import { getFileInfoById } from "../api/getFileInfoById";
import { useSelector } from "react-redux";


export function useGetFileInfoById(fileId) {
    const {userId, accessToken} = useSelector((state) => state.user)
    return useQuery({
        queryKey: ['file', fileId],
        queryFn: async () => (await getFileInfoById(accessToken, userId, fileId)),
    })
}