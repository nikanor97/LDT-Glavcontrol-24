
export const getFileId = (file:File) => {
    const hash = btoa(`${file.size}${file.type}${file.lastModified}`);
    return `${file.name}${hash}`;
};