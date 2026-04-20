
export async function extractCode(imageFile) {
    const formData = new FormData()     //formData is an object in js (like dict in python)
    //append file to formdata here
    formData.append("file",imageFile);
    // fetch to your backend here
   const response = await fetch("http://localhost:8000/upload", {
    method: "POST",
        body: formData
    })
    const data = await response.json()
    
    // return the result here
    return data
}