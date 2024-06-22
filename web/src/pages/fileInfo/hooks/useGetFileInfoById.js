import { useQuery } from "@tanstack/react-query";
import { getFileInfoById } from "../api/getFileInfoById";


export function useGetFileInfoById(fileId) {
    return useQuery({
        queryKey: ['file', fileId],
        queryFn: async () => (await getFileInfoById(fileId)),
        refetchOnWindowFocus: false,
    })
}