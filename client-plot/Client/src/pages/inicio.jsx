import React, { useState } from 'react';
import banner from '../assets/banner.jpg';
import Fondo_AI from '../assets/Fondo_AI.jpg';
import axios from 'axios';
import { RingLoader } from 'react-spinners';
import Swal from "sweetalert2";


export function Inicio() {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedOption, setSelectedOption] = useState('Seleccionar');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [startDateIn, setStartDateIn] = useState('');
  const [endDateIn, setEndDateIn] = useState('');
  const [batchSize, setBatchSize] = useState(5);
  const [ticker, setTicker] = useState('');
  const [imageSrc, setImageSrc] = useState(null);
  const [plotUrl, setPlotUrl] = useState('');
  const [trained, setTrained] = useState('');
  const [showImage, setShowImage] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [loadingState, setLoadingState] = useState('');
  const [isTwitter, setIsTwitter] = useState(false);
  const toggleMenu = () => setIsOpen(!isOpen);

  const handleSelect = (option) => {
    setSelectedOption(option);
    setIsOpen(false);

    if (option === 's&p500') {
      setBatchSize(25);
    } else if (option === 'downjones') {
      setBatchSize(2);
    } else if (option === 'twitter'){
      setIsTwitter(true)
    }
  };

  const trainModel = async () => {
    setIsLoading(true);
    setLoadingState('Entrenando el modelo...');
  
    console.log(`Selected Option ${selectedOption}`);
    console.log(`StartDate ${startDate}`);
    console.log(`EndDate ${endDate}`);
    console.log(`StartDateInference ${startDateIn}`);
    console.log(`EndDateInference ${endDateIn}`);
    console.log(`Batch Size ${batchSize}`);
    console.log(`Ticker ${ticker}`);
  
    const TrainData = {
      index: selectedOption,
      start_date: startDate,
      end_date: endDate,
      batch_size: batchSize,
    };
  
    try {
      if (selectedOption === 'twitter') {
        const R0 = await axios.get('/train/twitter', TrainData);
        console.log('Respuesta entrenamiento', R0.data); 
      } else {
        const R1 = await axios.post('/train/yahoofinance', TrainData);
        console.log('Respuesta entrenamiento', R1.data);
      }
      setTrained(true);
    } catch (error) {
      console.error('Error en el entrenamiento del modelo:', error);
      setTrained(false);
    } finally {
      setIsLoading(false);          
      setLoadingState('');          
    }
  };
  

  const inferences = async () =>{
    setIsLoading(true);          
    setLoadingState('Haciendo la inferencia...');  
    const InferenceDate = {
      ticker: ticker,
      start_date: startDateIn,
      end_date: endDateIn,
      index: selectedOption,
    };

    try {
      console.log(InferenceDate)
      const R2 = await axios.post('/inference/', InferenceDate);
      console.log('Respuesta Inferencia', R2.data);
      console.log('Respuesta Inferencia', R2.data.path);
      setPlotUrl(R2.data.path);
    } catch (error) {
      console.log("Error al hacer la inferencia")
    }finally {
      setIsLoading(false);          
      setLoadingState('');          
    }
    
  }

  const procesarFechasDeInicio = (start) => {
     
      setStartDateIn(start)
    
  }

  const procesarFechasDeFinalizacion = (end) => {
    
      setEndDateIn(end)
    
  }
  
  const obtenerGrafica = async (e) => {
    setIsLoading(true);          
    setLoadingState('Cargando imagen...'); 
    e.preventDefault();
    try {
      const response = await axios.post('/plot/',
        { url: plotUrl },
        { responseType: 'blob' }
      );
  
      const imageObjectURL = URL.createObjectURL(response.data);
      setImageSrc(imageObjectURL);
      setShowImage(true); 
    } catch (error) {
      console.error('Error al generar la gráfica:', error);
    }finally {
      setIsLoading(false);          
      setLoadingState('');          
    }
  };
  

  return (
    <div className="min-h-screen flex flex-col bg-cover bg-center" style={{ backgroundImage: `url(${Fondo_AI})` }}>
      <header className="py-8 px-8 flex justify-between items-center shadow-md"
        style={{ backgroundImage: `url(${banner})`, backgroundSize: 'cover', backgroundPosition: 'center' }}>
        <h1 className="text-6xl text-white font-bold">Predicciones IA</h1>
        <span className="text-5xl">🌐</span>
      </header>

      <div className="flex justify-center items-center p-8 min-h-[calc(100vh-160px)]">
        <form className="bg-white bg-opacity-80 backdrop-blur-sm p-8 rounded-xl shadow-lg w-full max-w-md space-y-6">

        {trained && (
          <button 
            type="button" 
            className="bg-blue-600 text-white py-2 px-4 rounded-full hover:bg-blue-700 transition" 
            onClick={() => {setTrained(false),setShowImage(false), setPlotUrl('')}}
            disabled={isLoading}>
            New Train
          </button>
        )}
            
          {/* Menú desplegable */}
          <div className="flex justify-between items-center relative">
            <label className="font-semibold">Data</label>
            <div className="ml-4 flex-1 relative">
              <button type="button" onClick={toggleMenu} className="w-full p-2 rounded text-black bg-gray-200 text-left">
                {selectedOption}
              </button>

              {isOpen && (
                <div className="absolute mt-2 w-full rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 z-10">
                  <div className="py-1">
                    <button type="button" onClick={() => handleSelect('s&p500')} className="block w-full text-left px-4 py-2 text-gray-700 hover:bg-gray-100">
                      s&p500
                    </button>
                    <button type="button" onClick={() => handleSelect('downjones')} className="block w-full text-left px-4 py-2 text-gray-700 hover:bg-gray-100">
                      Down Jones
                    </button>
                    <button type="button" onClick={() => handleSelect('nasdaq100')} className="block w-full text-left px-4 py-2 text-gray-700 hover:bg-gray-100">
                      Nasdaq-100
                    </button>
                    <button type="button" onClick={() => handleSelect('twitter')} className="block w-full text-left px-4 py-2 text-gray-700 hover:bg-gray-100">
                      Twitter
                    </button>
                    <button type="button" onClick={() => handleSelect('tsxcomposite')} className="block w-full text-left px-4 py-2 text-gray-700 hover:bg-gray-100">
                    tsxcomposite
                    </button>
                    <button type="button" onClick={() => handleSelect('ftse100')} className="block w-full text-left px-4 py-2 text-gray-700 hover:bg-gray-100">
                    ftse100
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>

          {trained && !isTwitter &&(
            <div className="flex justify-between items-center">
            <label className="font-semibold">Ticker</label>
            <input
              type="text"
              className="ml-4 flex-1 p-2 rounded text-black bg-gray-200"
              value={ticker}
              onChange={(e) => setTicker(e.target.value)}
            />
          </div>
          )}
          
          {/* Fechas */}
          {!trained && (
            <div className="flex justify-between items-center">
            <label className="font-semibold">Start Date Train</label>
            <input type="date" className="ml-4 flex-1 p-2 rounded text-black bg-gray-200"
              value={startDate} onChange={(e) => setStartDate(e.target.value)} />
          </div>
          )}
          
          {!trained &&(
            <div className="flex justify-between items-center">
            <label className="font-semibold">End Date Train</label>
            <input type="date" className="ml-4 flex-1 p-2 rounded text-black bg-gray-200"
              value={endDate} onChange={(e) => setEndDate(e.target.value)} />
          </div>
          )}
          
          {trained && (
            <div className="flex justify-between items-center">
              <label className="font-semibold">Start Date Inference</label>
              <input
                type="date"
                className="ml-4 flex-1 p-2 rounded text-black bg-gray-200"
                value={startDateIn}
                onChange={(e) => setStartDateIn(e.target.value)}  
                onBlur={(e) => procesarFechasDeInicio(e.target.value)} 
              />
            </div>
          )}

          {trained && (
            <div className="flex justify-between items-center">
              <label className="font-semibold">End Date Inference</label>
              <input
                type="date"
                className="ml-4 flex-1 p-2 rounded text-black bg-gray-200"
                value={endDateIn}
                onChange={(e) => setEndDateIn(e.target.value)} 
                onBlur={(e) => procesarFechasDeFinalizacion(e.target.value)} 
              />
            </div>
          )}
         
          {isLoading && (
            <div className="flex flex-col items-center">
              <RingLoader color="#34e7ed" size={150} />
              <p className="mt-2 text-blue-500 font-semibold">{loadingState}</p>
            </div>
          )}

          {/* Botones */}
          <div className="flex flex-col space-y-4 mt-8">
            {!showImage &&(
              <button 
              type="button" 
              className="bg-blue-600 text-white py-2 px-4 rounded-full hover:bg-blue-700 transition" 
              onClick={trainModel}
              disabled={isLoading}>
              Train Model
            </button>
            )}
      
            {trained && !showImage && (
              <button 
              type="button" 
              className="bg-blue-600 text-white py-2 px-4 rounded-full hover:bg-blue-700 transition" 
              onClick={inferences}
              disabled={isLoading}>
                Made Inference
              </button>
            )}           

            {plotUrl && !showImage && (
              <button 
              type="button" 
              onClick={obtenerGrafica} 
              className="bg-green-600 text-white py-2 px-4 rounded-full hover:bg-green-700 transition"
              disabled={isLoading}>
                Generate Gráphic
              </button>
            )}

          </div>
        </form>
      </div>

      {/* Imagen generada */}
      {showImage && (
        <div className="absolute top-0 left-0 w-full h-full flex justify-center items-center z-50">
          <div className="relative bg-white p-4 rounded-xl shadow-lg w-[99%] max-w-[1600px]">

            <button
              className="absolute top-4 right-4 bg-red-600 text-white py-2 px-4 rounded-full hover:bg-red-700 transition"
              onClick={() => setShowImage(false)}
            >
              Atrás
            </button>
            <img src={imageSrc} alt="Gráfica generada" className="rounded-lg w-full h-auto" />
          </div>
        </div>
      )}

    </div>
  );
}
