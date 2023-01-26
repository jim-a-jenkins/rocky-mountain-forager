import axios from 'axios';

class LibraryDataService {

    getAllPlants(){
        //axios.defaults.headers.common["Authorization"] = "Token " + token;
        return axios.get("/api/v1/plants");//?group=Trees
    }

    getTrees(){
        return axios.get("/api/v1/plants?group=Trees");
    }

    getShrubs(){
        return axios.get("/api/v1/plants?group=Shrubs");
    }

    getHerbs(){
        return axios.get("/api/v1/plants?group=Herbs");
    }

    getLichens(){
        return axios.get("/api/v1/plants?group=Lichens");
    }

    getPoisonous(){
        return axios.get("/api/v1/plants?poisonous=True");
    }
}

export default new LibraryDataService();