const librarianNavbarFromIndex = {
    Home: "../index.html",
    Add_Book: "./Pages/addBook.html",
    Remove_Book: "./Pages/removeBook.html",
};


const defaultNavbarFromIndex = {
    Home:"../index.html",
    Catalog: "./Pages/catalog.html",
    Storage: "./Pages/shoppingCart.html",
};

const librarianNavbarFromFolder = {
    Home: "../index.html",
    Add_Book: "./addBook.html",
    Remove_Book: "./removeBook.html",
};


const defaultNavbarFromFolder = {
    Home:"../index.html",
    Catalog: "./catalog.html",
    Storage: "./shoppingCart.html",
};

const setNavbar = (type) => {
    const page = sessionStorage.getItem('page');
    const navbarNode = document.getElementById('navbarSupportedContent');
    let navbar = '';

    if(type === 'defaultNavbar'){
        if(page === 'Home'){
            navbar = createString(defaultNavbarFromIndex,page);
        } else{
            navbar = createString(defaultNavbarFromFolder,page);
        }
    } else {
        if(page === 'Home'){
            navbar = createString(librarianNavbarFromIndex,page);
        } else{
            navbar = createString(librarianNavbarFromFolder,page);
        }
    }
    navbarNode.children[0].insertAdjacentHTML('afterbegin', navbar);
};
//aria-current="page"
const createNavbar = () => {
    const type = sessionStorage.getItem(status);
    console.log(window.location.pathname);

    if(type !== undefined){
        console.log(type);
        setNavbar(type);
        return;
    }
    console.log(444);
    const value = 'defaultNavbar';

    sessionStorage.setItem('status',value);
    sessionStorage.setItem('page','Home');

    setNavbar(value);
};

const changeRoute = (page) => {
    sessionStorage.setItem('page',page.name);
};
//href=${url}>${page}
const createString = (form,focusedPage) =>{
    let navBar = ``;
    Object.entries(form).forEach(([page,url]) => {
        if(focusedPage !== page){
            navBar += `<li class="nav-item"> <a class="nav-link" href=${url}  onclick = 'changeRoute(this)' name = ${page}>${page}</a></li>`;
        }else{
            navBar += `<li class="nav-item"> <a class="nav-link active" aria-current="page" href=${url} onclick = 'changeRoute(this) name = ${page})' >${page}</a> </li>`;
        }
    });
    console.log(navBar);
    return navBar;
};

createNavbar();