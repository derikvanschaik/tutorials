const runHandler = (output, code) =>{
    try{
        output.replaceRange("$ "+eval(`${code}`)+"\n", CodeMirror.Pos(output.lastLine() + 1) );
    }catch(e){
        output.replaceRange("$ "+e+"\n", CodeMirror.Pos(output.lastLine() + 1) );
    }
}
window.onload = () =>{ 
    const [code, out] = document.querySelectorAll(".codemirror-textarea"); 
    const run = document.querySelector("#run");
    const clear = document.querySelector("#clear"); 
    // configs
    const editor = CodeMirror.fromTextArea(code, {lineNumbers: true}); 
    const output = CodeMirror.fromTextArea(out, {lineNumbers: false}); 
 
    run.addEventListener("click", ()=>{
        const code = editor.getValue();
        runHandler(output, code);  
    });

    clear.addEventListener("click", ()=>{
        output.setValue(""); 
    }); 
} 