const defaultNavbar = `
<li class="nav-item"> <a class="nav-link " href="{{url_for('catalogue')}}">Каталог</a> </li>
<li class="nav-item"> <a class="nav-link " aria-current="page" href="{{url_for('basket')}}">Корзина</a> </li>`;

const librarianNavbar = `<li class="nav-item"> <a class="nav-link active" aria-current="page" href="{{url_for('addBook')}}">Додати книгу</a> </li>
<li class="nav-item"> <a class="nav-link " href="{{url_for('removeBook')}}">Видалити Книгу</a> </li>
<li class="nav-item"> <a class="nav-link " aria-current="page" href="{{url_for('page_for_returning_books')}}">Повернути книгу</a> </li>`;

const setNavbar = (type) => {
    const navbarNode = document.getElementById('navbarSupportedContent');
    if(type === 'reader'){
        navbarNode.children[0].insertAdjacentHTML('afterbegin', defaultNavbar);
    } else {
        navbarNode.children[0].insertAdjacentHTML('afterbegin', librarianNavbar);
    }
};
//aria-current="page"
const createNavbar = (role) => {
    const type = sessionStorage.getItem('status');

    if(type !== null && (!role || role === type)){
        setNavbar(type);
        return;
    }


    sessionStorage.setItem('status',role);

    setNavbar(role);
};
