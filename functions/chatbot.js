const { spawn } = require('child_process');
const path = require('path');

exports.handler = async function(event, context) {
  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      body: 'Method Not Allowed'
    };
  }

  try {
    const body = JSON.parse(event.body);
    const userInput = body.message;

    // Run the Python script
    const pythonProcess = spawn('python', [
      path.join(__dirname, '../run_chatbot.py'),
      userInput
    ]);

    let response = '';
    let error = '';

    pythonProcess.stdout.on('data', (data) => {
      response += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
      error += data.toString();
    });

    return new Promise((resolve, reject) => {
      pythonProcess.on('close', (code) => {
        if (code !== 0) {
          resolve({
            statusCode: 500,
            body: JSON.stringify({ error: 'Internal Server Error', details: error })
          });
        } else {
          resolve({
            statusCode: 200,
            body: JSON.stringify({ response })
          });
        }
      });
    });
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: error.message })
    };
  }
}; 