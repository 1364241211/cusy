import { compress } from 'image-conversion';

function imageCompress(data: File | undefined): string {
    let dataUrl = ""
    if (data !== undefined)
        compress(data, 200).then((value) => {
            const imageReader = new FileReader()
            imageReader.onload = (e) => {
                // console.log(e.target?.result);
                dataUrl = e.target?.result as string
                console.log(dataUrl);
            }
            imageReader.readAsDataURL(value)
        })
    console.log(dataUrl);
    return dataUrl
}
export default imageCompress
