const dragArea = document.querySelector('.drag-area');
const dragText = document.querySelector('.header');
let button = document.querySelector('.button');
let input = document.querySelector('.input');
let file;
button.onclick=() => {
    input.click();
};
input.addEventListener('change', function(){
    file = this.files[0];
    dragArea.classList.add('active');
    displayFile()
});
//when file is inside the drag area
dragArea.addEventListener('drag-area',(event) => {
    event.preventDefault();
    dragText.textContent='Release to upload';
    dragArea.classList.add('active');
    // console.log('file is inside the drag area');
});
//when file leaves the drag area 
dragArea.addEventListener('drop',(event) => {
    dragText.textContent='Drag & Drop';
    dragArea.classList.add('active');
});
//when the file is dropped in the drag area
dragArea.addEventListener('drop',(event) => {
    event.preventDefault();
    
    file = event.dataTransfer.files[0];
    //console.log(file);
    displayFile()
});
function displayFile(){
    let fileType = file.type;
    // console.log
    let validExtensions = ['image/jpeg', 'image/jpg', 'image/png']
    if(validExtensions.includes(fileType)){
        let fileReader = new fileReader();
        fileReader.onload = () =>{
            let fileurl = fileReader.result;
           // console.log(fileurl);
           let imgTag = '<img src="${fileurl}" alt="">';
           dragArea.innerHTML = imgTag;
        };
        fileReader.readAsDataURL(file);
        }else{
            alert('this file is not an image');
            dragArea.classList.remove('active');
        }
}
