const response = await fetch('http://localhost:8000/default/stream');
const readableStream = response.body;
const reader = readableStream.getReader();
while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    var text = new TextDecoder("utf-8").decode(value);
    console.log("Received ", text);
}