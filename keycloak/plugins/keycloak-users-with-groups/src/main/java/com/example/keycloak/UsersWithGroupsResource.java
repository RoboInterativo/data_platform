package com.example.keycloak;

import jakarta.ws.rs.*;
import jakarta.ws.rs.core.*;
import org.keycloak.models.*;
import org.keycloak.services.resource.RealmResourceProvider;
import org.keycloak.services.managers.AppAuthManager;
import org.keycloak.services.managers.AuthenticationManager.AuthResult;
import java.util.*;
import java.util.stream.Collectors;

public class UsersWithGroupsResource implements RealmResourceProvider {

    private final KeycloakSession session;

    public UsersWithGroupsResource(KeycloakSession session) {
        this.session = session;
    }

    @Override
    public Object getResource() {
        return this;
    }

    @GET
    @Path("")
    @Produces(MediaType.APPLICATION_JSON)
    public Response getUsersWithGroups() {
        try {
            // Проверка токена
            AuthResult auth = new AppAuthManager.BearerTokenAuthenticator(session)
                .authenticate();

            if (auth == null) {
                return Response.status(Response.Status.UNAUTHORIZED)
                       .entity(Map.of("error", "Authorization token required"))
                       .build();
            }

            RealmModel realm = session.getContext().getRealm();

            // Получаем и фильтруем пользователей
            List<Map<String, Object>> result = session.users()
                .searchForUserStream(realm, Map.of())
                .filter(user -> !isServiceAccount(user)) // Фильтруем service-аккаунты
                .map(this::mapUserWithGroups)
                .collect(Collectors.toList());

            return Response.ok(result).build();

        } catch (Exception e) {
            return Response.status(Response.Status.INTERNAL_SERVER_ERROR)
                   .entity(Map.of("error", e.getMessage()))
                   .build();
        }
    }

    private boolean isServiceAccount(UserModel user) {
        // Проверяем, является ли пользователь service-аккаунтом
        return user.getUsername() != null
               && user.getUsername().startsWith("service-account-");
    }

    private Map<String, Object> mapUserWithGroups(UserModel user) {
        Map<String, Object> userData = new HashMap<>();
        userData.put("id", user.getId());
        userData.put("username", user.getUsername());
        userData.put("enabled", user.isEnabled());

        // Добавляем createdTimestamp только если он > 0
        long createdTimestamp = user.getCreatedTimestamp();
        if (createdTimestamp > 0) {
            userData.put("createdTimestamp", createdTimestamp);
        }

        // Добавляем группы
        userData.put("groups", user.getGroupsStream()
            .map(group -> Map.of("id", group.getId(), "name", group.getName()))
            .collect(Collectors.toList()));

        // List<Map<String, String>> groups = user.getGroupsStream()
        //     .map(group -> Map.of(
        //         "id", group.getId(),
        //         "name", group.getName()
        //     ))
        //     .collect(Collectors.toList());
        //
        // if (!groups.isEmpty()) {
        //     userData.put("groups", groups);
        // }

        return userData;
    }

    @Override
    public void close() {}
}
