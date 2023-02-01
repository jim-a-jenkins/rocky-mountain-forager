import axios from 'axios';

class FlashcardsDataService {

    getAllScores(){
        const token = "4a1fd6889b45dd4c6bdcaf8ffb2bd214c3334907"
        axios.defaults.headers.common["Authorization"] = "Token " + token;
        return axios.get("/api/v1/scores");//?group=Trees
    }
}

export default new FlashcardsDataService();