const createSpans = (root, chars) =>{
    chars.forEach( (char, idx) =>{
        const span = document.createElement("span");
        span.textContent = char;
        span.setAttribute("id", idx); 
        root.appendChild(span);  
    }); 
}
const flashingCursor = () =>{
    return setInterval(() => {
        const cursor = document.getElementById(`${0}`); 
        if (cursor.style.color === "black"){
            cursor.style.color = 'white';
            cursor.style.backgroundColor = 'black'; 
        }else{
            cursor.style.color = 'black';
            cursor.style.backgroundColor = 'white';
        }
    }, 500); 
}
const getQuoteList = async () =>{
    const response = await fetch("https://type.fit/api/quotes"); 
    const data = await response.json(); 
    return data.map( obj => obj.text); 
}
const styleCursor = (cursorIdx, txtColor, bgColor) =>{
    const span = document.getElementById(`${cursorIdx}`); 
    span.style.color = txtColor;
    span.style.backgroundColor = bgColor; 
}
// main fucntion 
window.onload = async () =>{
    const root = document.querySelector("#root");
    let curQuoteIdx = 0;
    let quotesList = await getQuoteList(); 
    let displayText = quotesList[curQuoteIdx].toLowerCase().split(""); 
    createSpans(root, displayText); 
    let cursor = 0; 
    let flash = flashingCursor();

    window.addEventListener("keydown", (event) =>{
        if (flash){
            clearInterval(flash);
            flash = null; 
        }
        if (event.key === displayText[cursor]){
            cursor++;
            styleCursor(cursor -1, 'black', 'white');  
        }
        if (cursor < displayText.length){
            return styleCursor(cursor, 'white', 'black'); 
        }
        // user type entire sentence -- reload variables 
        displayText = quotesList[++curQuoteIdx].toLowerCase().split(""); 
        root.replaceChildren(); 
        createSpans(root, displayText); 
        cursor = 0; 
        flash = flashingCursor(); 
    })

}