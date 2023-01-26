import React, {useState, useEffect} from 'react';
import LibraryDataService from '../services/library-service'; //TODO

const Library = props => {
    const[trees, setTrees] = useState([]);
    const[herbs, setHerbs] = useState([]);
    const[shrubs, setShrubs] = useState([]);
    const[lichens, setLichens] = useState([]);
    const[poisonous, setPoisonous] = useState([]);

    useEffect(() =>{
        retrievePlants();
    }, [props.token]);

    const retrievePlants = () => {
        // TODO refactor to avoid repetitive code
        LibraryDataService.getTrees(props.token)
        .then(response => {
            setTrees(response.data);
        })
        .catch( e => {
            console.log(e);
        });

        LibraryDataService.getHerbs(props.token)
        .then(response => {
            setHerbs(response.data);
        })
        .catch( e => {
            console.log(e);
        });

        LibraryDataService.getShrubs(props.token)
        .then(response => {
            setShrubs(response.data);
        })
        .catch( e => {
            console.log(e);
        });

        LibraryDataService.getLichens(props.token)
        .then(response => {
            setLichens(response.data);
        })
        .catch( e => {
            console.log(e);
        });

        LibraryDataService.getPoisonous(props.token)
        .then(response => {
            setPoisonous(response.data);
        })
        .catch( e => {
            console.log(e);
        });
    }

    const List = ({list}) => (
        <ul>
            {list.map((item) => (
                <Item
                    key={item.objectID}
                    item={item}
                />
            ))}
        </ul>
    );
    
    const Item = ({item}) => (
        <li className='item'>
            <span style={{ width: '30%' }}>{item.name}</span>
        </li>
    );

    return(
        <header className='App-header'>
            <h1>Table of Contents</h1>
            <h2>Trees</h2>
            <List
                list={trees}
            />
            <h2>Shrubs</h2>
            <List
                list={shrubs}
            />
            <h2>Herbs</h2>
            <List
                list={herbs}
            />
            <h2>Lichens</h2>
            <List
                list={lichens}
            />
            <h2>Poisonous Look-Alikes</h2>
            <List
                list={poisonous}
            />
          </header>
    );
}

export default Library;