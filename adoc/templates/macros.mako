<%def name="anchor(atom)">
  id="${atom.fully_qualified_name}"
</%def>

<%def name="link(atom)">
  <a href="#${atom.fully_qualified_name}">
    ${text or atom.name}
  </a>
</%def>

<%def name="show_inheritance(d)">
  % if hasattr(d, 'inherits'):
    <p class="inheritance">
     <strong>Inheritance:</strong>
     % if hasattr(d.inherits, 'cls'):
       <code>${link(d.inherits.cls.refname)}</code>.<code>${link(d.inherits.refname)}</code>
     % else:
       <code>${link(d.inherits.refname)}</code>
     % endif
    </p>
  % endif
</%def>

<%def name="show_modules(modules)">
  % for module in modules:
    <section class="section-items">
      <h2 class="section-title" ${anchor(module)}>
        Module <code>${module.fully_qualified_name}</code>
      </h2>

      ${format_doc(module)}

      % if module.functions:
        <h2 class="section-title">
          Functions
        </h2>

        ${show_functions(module.functions)}
      % endif

      % if module.classes:
        <h2 class="section-title">
          Classes
        </h2>

        ${show_classes(module.classes)}
      % endif
    </section>

    % if module.modules:
      ${show_modules(module.modules)}
    % endif
  % endfor
</%def>

<%def name="show_functions(functions)">
  % for function in functions:
    <div class="item">
      <div class="name def" ${anchor(function)}>
        % if function.decorators:
          % for decorator in function.decorators:
            <div>@${decorator.name}</div>
          % endfor
        % endif

        <div>
          <p>def <span class="ident">${function.name}</span>(</p>
          % if function.parameters:
            <p>${', '.join([p.to_html() for p in function.parameters])})</p>
          % else:
            <p>)</p>
          % endif
        </div>
      </div>

      <div class="desc">
        ${format_doc(function)}
      </div>
    </div>
  % endfor
</%def>

<%def name="show_classes(classes)">
  % for klass in classes:
    <div class="item">
      <p class="name" ${anchor(klass)}>
        % if klass.decorators:
          % for decorator in klass.decorators:
            @${decorator.name}<br>
          % endfor
        % endif

        class <span class="ident">${klass.name}</span>
      </p>

      <div class="desc">
        ${format_doc(klass)}
      </div>

      <div class="class">
        % if klass.bases:
          <h3>
            Ancestors
          </h3>

          <ul class="class_list">
            % for base in klass.bases:
              <li class="mono">
                <a href="#ancestors">${base}</a>
              </li>
            % endfor
          </ul>
        % endif

        % if klass.functions:
          <h3>
            Methods
          </h3>

          ${show_functions(klass.functions)}
        % endif
      </div>
    </div>
  % endfor
</%def>

<%def name="list_modules(modules)">
  <ul>
    % for module in modules:
      <li class="mono">
        ${link(module)}

        % if module.modules:
          ${list_modules(module.modules)}
        % endif
      </li>
  % endfor
  </ul>
</%def>

<%def name="list_functions(project)">
    % for function in project.iter_functions():
        <li class="mono">
            ${link(function)}
        </li>
    % endfor
</%def>

<%def name="list_classes(modules)">
    % for klass in project.iter_classes():
        <li class="mono">
            ${link(klass)}
        </li>
    % endfor
</%def>

<%def name="show_doc(article)">
  <section>
    ${format_doc(article)}
  </section>
</%def>
