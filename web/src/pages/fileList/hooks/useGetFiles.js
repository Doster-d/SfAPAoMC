import { useInfiniteQuery } from "@tanstack/react-query";
import { getFiles } from "../api/getFiles";

export function useGetFiles() {
  return useInfiniteQuery({
    queryKey: ["files"],
    queryFn: getFiles,
    initialPageParam: 0,
    getNextPageParam: (lastPage, _, lastPageParam) => {
        if(lastPage.length === 0) {
            return undefined;
        }
        return lastPageParam + 1;
    },
    getPreviousPageParam: (_, __, firstPageParam) => {
        if(firstPageParam <= 1) {
            return undefined
        }
        return firstPageParam - 1
    }
  });
}
