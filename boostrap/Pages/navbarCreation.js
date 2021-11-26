const defaultNavbar = `
<li class="nav-item"> <a class="nav-link " href="{{url_for('catalogue')}}">Каталог</a> </li>
<li class="nav-item"> <a class="nav-link " aria-current="page" href="{{url_for('basket')}}">Корзина</a> </li>
<li class="nav-item" id = 'orders'> <a class="nav-link " aria-current="page" href="{{url_for('page_for_orders')}}">Замовлення</a> </li>`;

const librarianNavbar = {
    'add books' : `<li class="nav-item"> <a class="nav-link" aria-current="page" href="{{url_for('addBook')}}">Додати книгу</a> </li>`,
    'delete books': `<li class="nav-item" id = 'delete books'> <a class="nav-link " href="{{url_for('removeBook')}}">Видалити Книгу</a> </li>`,
    'issue/accept books' : `<li class="nav-item" id = 'issue/accept books'> <a class="nav-link " aria-current="page" href="{{url_for('issuebooks')}}">Видати книгу</a> </li>`,
};

const setNavbar = (type, permissions) => {
    const navbarNode = document.getElementById('navbarSupportedContent');
    if(type === 'reader'){
        navbarNode.children[0].insertAdjacentHTML('afterbegin', defaultNavbar);
    } else {
        permissions.forEach(permission => {
            navbarNode.children[0].insertAdjacentHTML('afterbegin',librarianNavbar[permission]);
        });
        navbarNode.children[0].insertAdjacentHTML('afterbegin',`<li class="nav-item"> <a class="nav-link " aria-current="page" href="{{url_for('page_for_returning_books')}}">Повернути книгу</a> </li>`);
    }
};
//aria-current="page"
const createNavbar = () => {
    let role = sessionStorage.getItem('status');
    let permissions = sessionStorage.getItem('permissions');

    if(!permissions){
        permissions = [];
    }

    if(!role){
        role ='reader';
    }

    if (typeof permissions === 'string'){
        setNavbar(role,permissions.split(','));
    } else{
        setNavbar(role,permissions);
    }
};
