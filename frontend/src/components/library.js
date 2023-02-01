import React, {useState, useEffect} from 'react';
import Button from 'react-bootstrap/Button';
import Offcanvas from 'react-bootstrap/Offcanvas';
import LibraryDataService from '../services/library-service';

const Library = props => {
    const[trees, setTrees] = useState([]);
    const[herbs, setHerbs] = useState([]);
    const[shrubs, setShrubs] = useState([]);
    const[lichens, setLichens] = useState([]);
    const[poisonous, setPoisonous] = useState([]);

    // Offcanvas
    const [show, setShow] = useState(false);
    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

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
            <Button variant="primary" onClick={handleShow}>
                Show Library
            </Button>
            <Offcanvas show={show} onHide={handleClose} backdrop={false} scroll={true}>
                <Offcanvas.Header closeButton>
                <Offcanvas.Title><h2>Library of Plants</h2></Offcanvas.Title>
                </Offcanvas.Header>
                <Offcanvas.Body>
                    <h2>Table of Contents</h2>
                    <h4>Trees</h4>
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
                </Offcanvas.Body>
            </Offcanvas>
          </header>
    );
}

export default Library;